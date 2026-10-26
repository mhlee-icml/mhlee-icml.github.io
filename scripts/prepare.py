"""Prepare Jekyll data from the preserved ICML content, without editing sources.

Run from any directory with Python 3.10 or later. Only generated _data/lab.json
and _pages wrappers are written. The source content remains the authority.
"""

from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
NEWS_KEYS = [
    "title", "date", "image", "source", "source_title", "source_url",
    "source_date", "date_source_url",
]


def read_json(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def read_document(path: str | Path) -> tuple[dict, str]:
    """Read the deliberately simple scalar front matter used in content/."""
    text = (ROOT / path).read_text(encoding="utf-8-sig")
    if not text.startswith("---\n"):
        return {}, text.strip()
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"Unclosed front matter: {path}")
    metadata = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator or not re.fullmatch(r"[a-z_]+", key):
            raise ValueError(f"Unsupported front matter in {path}: {line}")
        value = value.strip()
        if value.startswith('"') or value in ("null", "true", "false"):
            metadata[key] = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            metadata[key] = value[1:-1].replace("''", "'")
        else:
            metadata[key] = value
    return metadata, parts[2].strip()


class TextReader(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def plain_text(value: str) -> str:
    parser = TextReader()
    parser.feed(value)
    return " ".join(" ".join(parser.parts).split())


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", plain_text(value).lower()).strip("-")


def render_markdown(body: str) -> str:
    """Render the source's paragraph/link format and retain trusted raw HTML.

    News is intentionally restricted to its documented two-paragraph-and-link
    format. Existing biographies may contain <br>; preserve those tags. This
    is not a general-purpose Markdown implementation.
    """
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", body.strip()):
        # Preserve the existing biography HTML rather than double-escaping it.
        if re.match(r"\s*<(?:p|section|div|ul|ol|h[1-6])(?:\s|>)", paragraph):
            paragraphs.append(paragraph)
            continue
        fragments = []
        position = 0
        for match in re.finditer(r"\[([^\]]+)\]\((https?://[^\s)]+)\)|<br\s*/?>", paragraph):
            fragments.append(html.escape(paragraph[position:match.start()], quote=False))
            if match.group(1) is not None:
                fragments.append(
                    '<a href="' + html.escape(match.group(2), quote=True) + '">'
                    + html.escape(match.group(1), quote=False) + "</a>"
                )
            else:
                fragments.append(match.group(0))
            position = match.end()
        fragments.append(html.escape(paragraph[position:], quote=False))
        paragraphs.append("<p>" + "".join(fragments) + "</p>")
    return "\n".join(paragraphs)


def sections(body: str) -> list[dict]:
    result = []
    for match in re.finditer(r"<section>\s*<h2>(.*?)</h2>.*?</section>", body, re.S):
        title = plain_text(match.group(1))
        section_id = slugify(title)
        original = match.group(0)
        rendered = original.replace("<section>", f'<section id="{section_id}">', 1)
        result.append({"id": section_id, "title": title, "html": rendered, "original_html": original})
    return result


def source_hashes() -> dict[str, str]:
    paths = [p for directory in ("content", "assets/img") for p in (ROOT / directory).rglob("*") if p.is_file()]
    return {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(paths)
    }


def build_data() -> dict:
    site = read_json("content/site.json")
    _, professor_body = read_document("content/pages/professor.md")
    _, research_body = read_document("content/pages/research-fields.md")
    professor_sections = sections(professor_body)
    research_sections = sections(research_body)
    professor_html = professor_body
    research_html = research_body
    for section in professor_sections:
        professor_html = professor_html.replace(section["original_html"], section["html"], 1)
    for section in research_sections:
        research_html = research_html.replace(section["original_html"], section["html"], 1)

    section_map = {section["id"]: section["html"] for section in professor_sections}
    publications = section_map["publications"]
    selected_match = re.search(r"<h3>Selected Publications</h3>\s*<ul>(.*?)</ul>", publications, re.S)
    selected = [{"html": item.strip()} for item in re.findall(r"<li>(.*?)</li>", selected_match.group(1), re.S)]
    categories = []
    for category in re.finditer(r"<details>\s*<summary>(.*?)</summary>\s*<ul>(.*?)</ul>\s*</details>", publications, re.S):
        name = plain_text(category.group(1))
        entries = [{"html": item.strip()} for item in re.findall(r"<li>(.*?)</li>", category.group(2), re.S)]
        categories.append({"id": slugify(name), "title": name, "items": entries, "count": len(entries)})

    fields = []
    for section in research_sections:
        image = re.search(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"', section["html"])
        fields.append({
            "id": section["id"], "title": section["title"], "html": section["html"],
            "image": image.group(1), "alt": image.group(2),
        })

    people = []
    for person in read_json("content/people.json"):
        biography_html = ""
        if person.get("biography"):
            _, biography = read_document(person["biography"])
            biography_html = render_markdown(biography)
        people.append({**person, "biography_html": biography_html})

    join_us_html = ""
    if (ROOT / "content/pages/join-us.md").is_file():
        _, join_us_html = read_document("content/pages/join-us.md")

    news = []
    months = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    for path in sorted((ROOT / "content/news").glob("*.md")):
        metadata, body = read_document(path)
        if list(metadata) != NEWS_KEYS:
            raise ValueError(f"News metadata must follow the README format: {path.name}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md", path.name):
            raise ValueError(f"News filename must be YYYY-MM-DD-slug.md: {path.name}")
        for key in ("date", "source_date"):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata[key]):
                raise ValueError(f"Invalid {key}: {path.name}")
        year, month, day = metadata["date"].split("-")
        news.append({
            **metadata, "slug": path.stem, "path": f"/news/{path.stem}/",
            "html": render_markdown(body),
            "display_date": f"{months[int(month)]} {int(day):02d}, {year}",
        })
    news.sort(key=lambda item: (item["date"], item["slug"]), reverse=True)

    return {
        "site": site,
        "people": people,
        "join_us_html": join_us_html,
        "videos": read_json("content/videos.json"),
        "platforms": read_json("content/platforms.json"),
        "professor_html": professor_html,
        "professor_intro_html": professor_body.split("<section>", 1)[0].strip(),
        "professor_sections": section_map,
        "professor_navigation": [{"id": item["id"], "title": item["title"]} for item in professor_sections],
        "research_html": research_html,
        "research_fields": fields,
        "publications_html": publications,
        "publication_categories": categories,
        "selected_publications": selected,
        "projects_html": section_map["research-experience-and-projects"],
        "news": news,
        "source_hashes": source_hashes(),
    }


def write_page(path: Path, metadata: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front_matter = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
    path.write_text("---\n" + front_matter + "\n---\n", encoding="utf-8", newline="\n")


def main() -> None:
    data = build_data()
    (ROOT / "_data").mkdir(exist_ok=True)
    (ROOT / "_data/lab.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    # Capture a local, first-run preservation baseline. It is deliberately not
    # refreshed by subsequent preparation so unintended edits stay detectable.
    baseline = ROOT / ".cache/icml-content-baseline.json"
    if not baseline.exists():
        baseline.parent.mkdir(exist_ok=True)
        baseline.write_text(json.dumps(data["source_hashes"], indent=2) + "\n", encoding="utf-8")
    pages = [
        ("research-fields", "Research", "research", "research"),
        ("projects", "Research Projects", "projects", "research"),
        ("publications", "Publications", "publications", "publications"),
        ("professor", "Professor", "professor", "people"),
        ("people", "People", "people", "people"),
        ("alumni", "Alumni", "people", "people"),
        ("news", "News", "news-list", "news"),
        ("videos", "Research in Motion", "videos", "research"),
        ("join-us", "Join Us", "join-us", "join-us"),
    ]
    for slug, title, layout, nav in pages:
        write_page(ROOT / "_pages" / f"{slug}.md", {
            "layout": layout, "title": title, "permalink": f"/{slug}/", "nav": nav,
        })
    for item in data["news"]:
        write_page(ROOT / "_pages/news" / f"{item['slug']}.md", {
            "layout": "news", "title": item["title"], "permalink": item["path"],
            "nav": "news", "news_slug": item["slug"],
        })
    print(f"Prepared {len(pages) + len(data['news'])} pages; "
          f"{sum(category['count'] for category in data['publication_categories'])} publications, "
          f"{len(data['research_fields'])} research fields, {len(data['news'])} news stories.")


if __name__ == "__main__":
    main()
