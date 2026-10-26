"""Check preserved content and, when present, all local links in _site/."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

from prepare import ROOT, NEWS_KEYS, build_data, plain_text, read_document, source_hashes


class Document(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.images: list[dict] = []
        self.people: list[dict] = []
        self._depth = 0
        self._person_stack: list[tuple[int, dict]] = []
        self.feed(source)
        for person in self.people:
            person["text"] = " ".join(" ".join(person.pop("text_parts")).split())

    VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        if tag not in self.VOID_ELEMENTS:
            self._depth += 1
        values = dict(attributes)
        if values.get("id"):
            self.ids.append(values["id"])
        for attribute in ("href", "src", "poster"):
            if values.get(attribute):
                self.links.append(values[attribute])
        if tag == "img":
            self.images.append(values)
        if values.get("data-person-name"):
            person = {
                key: values.get("data-person-" + key, "")
                for key in ("name", "group", "role", "status")
            }
            person["text_parts"] = []
            self.people.append(person)
            self._person_stack.append((self._depth, person))

    def handle_data(self, data: str) -> None:
        for _, person in self._person_stack:
            person["text_parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.VOID_ELEMENTS:
            return
        while self._person_stack and self._person_stack[-1][0] >= self._depth:
            self._person_stack.pop()
        self._depth = max(0, self._depth - 1)


def check_sources(data: dict, errors: list[str]) -> None:
    current = source_hashes()
    if data["source_hashes"] != current:
        errors.append("Generated data is stale; run python scripts/prepare.py.")
    baseline_path = ROOT / ".cache/icml-content-baseline.json"
    if baseline_path.exists():
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        changed = [name for name in baseline if current.get(name) != baseline[name]]
        if changed:
            errors.append("Preserved source changed since the first build: " + ", ".join(changed))
    expected = build_data()
    if data != expected:
        errors.append("Generated lab data does not match the preserved content.")
    if sum(category["count"] for category in data["publication_categories"]) != 30:
        errors.append("Expected 30 full-list publications (the six selected entries are duplicates).")
    if len(data["selected_publications"]) != 6:
        errors.append("Expected all six selected-publication entries.")
    if len(data["research_fields"]) != 3:
        errors.append("Expected all three research fields.")
    if len(re.findall(r"<img\b", data["research_html"])) != 10:
        errors.append("Expected all ten research images.")
    for document in [data["professor_html"], data["research_html"], *(item["html"] for item in data["news"])]:
        for link in Document(document).links:
            if link.startswith("/assets/") and not (ROOT / link.lstrip("/")).is_file():
                errors.append(f"Missing original image: {link}")
    for person in data["people"]:
        for key in ("image", "biography"):
            if person.get(key) and not (ROOT / person[key].lstrip("/")).is_file():
                errors.append(f"Missing {key} for {person['name']}")
    for path in (ROOT / "content/news").glob("*.md"):
        metadata, body = read_document(path)
        if list(metadata) != NEWS_KEYS or len(re.split(r"\n\s*\n", body)) != 3:
            errors.append(f"News format differs from README: {path.name}")


def check_build(output: Path, data: dict, errors: list[str]) -> tuple[int, int]:
    files = sorted(output.rglob("*.html"))
    parsed = {path.resolve(): Document(path.read_text(encoding="utf-8")) for path in files}
    checked = 0
    for path, document in parsed.items():
        relative = path.relative_to(output.resolve()).as_posix()
        if len(document.ids) != len(set(document.ids)):
            errors.append(f"Duplicate IDs: {relative}")
        for image in document.images:
            if "alt" not in image:
                errors.append(f"Image lacks alt text: {relative}: {image.get('src')}")
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith("//"):
                continue
            target_url = urlsplit(urljoin("/" + relative, link))
            target = (output / unquote(target_url.path).lstrip("/")).resolve()
            if target.is_dir():
                target = target / "index.html"
            checked += 1
            if not target.is_file():
                errors.append(f"Broken local link: {relative} -> {link}")
                continue
            if target_url.fragment and target.suffix == ".html":
                target_document = parsed.get(target)
                if target_document and unquote(target_url.fragment) not in target_document.ids:
                    errors.append(f"Broken fragment: {relative} -> {link}")

    def require_text(relative: str, source_html: str, description: str) -> None:
        path = output / relative
        if not path.is_file():
            errors.append(f"Missing page: {relative}")
        elif plain_text(source_html) not in plain_text(path.read_text(encoding="utf-8")):
            errors.append(f"Incomplete {description}: {relative}")

    require_text("professor/index.html", data["professor_html"], "professor source text")
    require_text("research-fields/index.html", data["research_html"], "research source text")
    require_text("projects/index.html", data["projects_html"], "project source text")
    if data.get("join_us_html"):
        require_text("join-us/index.html", data["join_us_html"], "recruitment source text")
    # The publications page may rearrange categories, so verify every original
    # entry independently while keeping the exact full professor source above.
    for category in data["publication_categories"]:
        for item in category["items"]:
            require_text("publications/index.html", item["html"], "publication entry")
    for item in data["news"]:
        require_text(item["path"].lstrip("/") + "index.html", item["html"], "news body")
    videos_path = output / "videos/index.html"
    video_markup = videos_path.read_text(encoding="utf-8") if videos_path.is_file() else ""
    for video in data["videos"]:
        if video["path"] not in video_markup or video["caption"] not in plain_text(video_markup):
            errors.append(f"Missing video URL/caption: {video['title']}")
    people_path = output / "people/index.html"
    people_markup = people_path.read_text(encoding="utf-8") if people_path.is_file() else ""
    rendered_people = Document(people_markup).people
    expected_names = [person["name"] for person in data["people"]]
    rendered_names = [person["name"] for person in rendered_people]
    if sorted(rendered_names) != sorted(expected_names):
        errors.append("People page member cards do not match the source member list.")
    for group in dict.fromkeys(person["group"] for person in data["people"]):
        expected_order = [person["name"] for person in data["people"] if person["group"] == group]
        rendered_order = [person["name"] for person in rendered_people if person["group"] == group]
        if rendered_order != expected_order:
            errors.append(f"Member order differs from source for {group}.")
    if any(person["group"] == "undergraduate" for person in data["people"]):
        if "Undergraduate researchers" not in plain_text(people_markup):
            errors.append("Missing undergraduate researchers heading on the people page.")
    for person in data["people"]:
        if person["name"] not in plain_text(people_markup):
            errors.append(f"Missing registered person: {person['name']}")
        if person.get("image") and person["image"] not in people_markup:
            errors.append(f"Missing registered image: {person['name']}")
        if person["biography_html"] and plain_text(person["biography_html"]) not in plain_text(people_markup):
            errors.append(f"Missing registered biography: {person['name']}")
        rendered = next((item for item in rendered_people if item["name"] == person["name"]), {})
        for key in ("group", "role", "status"):
            if person.get(key) and rendered.get(key) != person[key]:
                errors.append(f"Member {key} differs from source: {person['name']}")
        if person.get("role") and person["role"].lower() not in rendered.get("text", "").lower():
            errors.append(f"Member role is not visible: {person['name']}")
        if person.get("status") == "incoming" and "Incoming" not in rendered.get("text", ""):
            errors.append(f"Incoming member status is not visible: {person['name']}")
        if person.get("status") == "current" and "Incoming" in rendered.get("text", ""):
            errors.append(f"Current member incorrectly shown as incoming: {person['name']}")
        for key in ("department", "department_ko"):
            if person.get(key) and person[key] not in rendered.get("text", ""):
                errors.append(f"Member {key} is missing: {person['name']}")
        if person["group"] == "alumni":
            require_text("alumni/index.html", person["name"], "alumni name")
    alumni_path = output / "alumni/index.html"
    if alumni_path.is_file():
        alumni_cards = Document(alumni_path.read_text(encoding="utf-8")).people
        if any(person["group"] != "alumni" for person in alumni_cards):
            errors.append("Alumni page includes a member outside the alumni group.")
    for original in (ROOT / "assets/img").iterdir():
        if original.is_file():
            built = output / "assets/img" / original.name
            if not built.is_file() or hashlib.sha256(original.read_bytes()).digest() != hashlib.sha256(built.read_bytes()).digest():
                errors.append(f"Built image is missing or altered: {original.name}")
    return len(files), checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--require-build", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    data_path = ROOT / "_data/lab.json"
    if not data_path.exists():
        raise SystemExit("Run python scripts/prepare.py first.")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    check_sources(data, errors)
    pages = links = 0
    if (args.output / "index.html").exists():
        pages, links = check_build(args.output.resolve(), data, errors)
    elif args.require_build:
        errors.append("Built index.html is missing.")
    if errors:
        for message in errors:
            print("ERROR: " + message)
        raise SystemExit(1)
    print(f"PASS: {len(data['source_hashes'])} preserved source files; "
          f"30 publications; 3 research fields / 10 images; "
          f"{len(data['people'])} registered person; {len(data['videos'])} videos; "
          f"{len(data['news'])} news stories.")
    if pages:
        print(f"PASS: {pages} HTML pages and {links} local links; "
              "original text and image bytes preserved.")
    else:
        print("Build checks skipped: _site/index.html does not exist yet.")


if __name__ == "__main__":
    main()
