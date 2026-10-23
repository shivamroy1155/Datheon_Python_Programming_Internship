"""Safely organize files into extension-based folders.

Usage:
    python organizer.py "C:/Users/YourName/Downloads"
    python organizer.py ./organizer_test --dry-run
By default, files are moved. Use --dry-run to preview first.
"""
import argparse
import logging
import shutil
from pathlib import Path

CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".json", ".xml", ".ipynb"},
}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def unique_destination(destination: Path) -> Path:
    """Avoid overwriting existing files by adding a numbered suffix."""
    if not destination.exists():
        return destination
    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> tuple[int, int]:
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Not a valid directory: {folder}")

    moved = skipped = 0
    for item in folder.iterdir():
        # Only process files directly inside the selected folder; don't recurse into category folders.
        if not item.is_file():
            continue
        target_dir = folder / category_for(item)
        target = unique_destination(target_dir / item.name)

        if dry_run:
            print(f"[DRY RUN] {item.name} -> {target.relative_to(folder)}")
            moved += 1
            continue

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))
            logging.info("Moved %s -> %s", item.name, target.relative_to(folder))
            moved += 1
        except (PermissionError, OSError) as exc:
            logging.error("Could not move %s: %s", item.name, exc)
            skipped += 1

    print("\n=== Organizer Summary ===")
    print(f"Folder: {folder.resolve()}")
    print(f"{'Would move' if dry_run else 'Moved'}: {moved}")
    print(f"Skipped/errors: {skipped}")
    return moved, skipped


def main():
    parser = argparse.ArgumentParser(description="Organize files by file extension.")
    parser.add_argument("folder", type=Path, help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        organize(args.folder.expanduser(), args.dry_run)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
