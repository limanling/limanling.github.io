#!/usr/bin/env python3
import re
from pathlib import Path

MARKERS = {
    "NAV": ("<!-- SHARED NAV START -->", "<!-- SHARED NAV END -->"),
    "SIDEBAR": ("<!-- SHARED SIDEBAR START -->", "<!-- SHARED SIDEBAR END -->"),
}


def extract_block(text: str, start_marker: str, end_marker: str) -> str:
    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"Could not find block between {start_marker} and {end_marker}")
    return match.group(0)


def update_file(path: Path, template_blocks: dict[str, str]) -> bool:
    text = path.read_text()
    updated = text
    for name, (start_marker, end_marker) in MARKERS.items():
        block = template_blocks[name]
        pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.S)
        if not pattern.search(updated):
            raise RuntimeError(f"{name} markers are missing in {path}")
        updated = pattern.sub(block, updated, count=1)
    if updated != text:
        path.write_text(updated)
        print(f"Updated {path}")
        return True
    return False


def main() -> None:
    shared = Path("shared-layout.html").read_text()
    template_blocks = {
        name: extract_block(shared, start, end)
        for name, (start, end) in MARKERS.items()
    }

    targets = [
        Path("index.html"),
        Path("students/index.html"),
    ]

    for target in targets:
        update_file(target, template_blocks)


if __name__ == "__main__":
    main()

