"""Build or preview the ICML site without publishing anything."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(arguments: list[str], env: dict | None = None) -> None:
    subprocess.run(arguments, cwd=ROOT, env=env, check=True)


def build() -> None:
    run([sys.executable, "scripts/prepare.py"])
    portable = sorted((ROOT / ".tools").glob("rubyinstaller-*/bin/ruby.exe"))
    if portable:
        ruby = portable[-1]
        env = os.environ.copy()
        env["PATH"] = str(ruby.parent) + os.pathsep + env.get("PATH", "")
        run([str(ruby), "scripts/build_jekyll.rb"], env=env)
    else:
        bundle = shutil.which("bundle") or shutil.which("bundle.bat")
        if not bundle:
            raise SystemExit("Ruby/Bundler is required. See README.md, then run bundle install.")
        run([bundle, "exec", "jekyll", "build"])
    run([sys.executable, "scripts/validate.py", "--require-build"])


def serve(port: int) -> None:
    output = ROOT / "_site"
    if not (output / "index.html").is_file():
        raise SystemExit("Build first: python scripts/site.py build")
    handler = partial(SimpleHTTPRequestHandler, directory=str(output))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError as exc:
        raise SystemExit(f"Cannot listen on port {port}: {exc}. Try --port 8766.")
    print(f"ICML local preview: http://127.0.0.1:{port}/", flush=True)
    print("Press Ctrl+C to stop. Only the generated _site directory is served.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "serve", "preview"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.command in ("build", "preview"):
        build()
    if args.command in ("serve", "preview"):
        serve(args.port)
