"""A simple CLI tool to organize files in a folder by extension."""

import shutil
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()

# File extension categories
DIRECTORIES: dict[str, list[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Code": [".py", ".json", ".html", ".css", ".js", ".cpp"],
}


def get_category(extension: str) -> str:
    """Return the folder category for a given file extension."""
    ext = extension.lower()
    for category, extensions in DIRECTORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_directory(target_path: Path) -> dict[str, int]:
    """Scan the target directory and move files into categorized folders."""
    if not target_path.exists() or not target_path.is_dir():
        raise ValueError(f"Invalid directory path: {target_path}")

    counts: dict[str, int] = {}

    for item in target_path.iterdir():
        # Only process files, ignore existing directories
        if item.is_file():
            category = get_category(item.suffix)
            dest_dir = target_path / category
            dest_dir.mkdir(exist_ok=True)

            shutil.move(str(item), str(dest_dir / item.name))
            counts[category] = counts.get(category, 0) + 1

    return counts


def main() -> None:
    console.print(
        "[bold cyan]📁 File Cleaner & Organizer[/bold cyan]", justify="center"
    )

    path_input = console.input(
        "\n[yellow]Enter folder path to organize (or press Enter for test-folder): [/yellow]"
    ).strip()

    target = Path(path_input) if path_input else Path("./test-folder")

    # If test folder doesn't exist, create it with sample dummy files
    if not target.exists():
        console.print(
            f"[dim]Directory '{target}' not found. Creating a sample test folder with dummy files...[/dim]"
        )
        target.mkdir(exist_ok=True)
        (target / "sample_report.pdf").touch()
        (target / "vacation_photo.jpg").touch()
        (target / "script_backup.py").touch()
        (target / "assets_bundle.zip").touch()
        (target / "notes.txt").touch()

    results = organize_directory(target)

    # Render results in a terminal table
    table = Table(title="Clean-up Summary")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Files Moved", style="magenta")

    for cat, count in results.items():
        table.add_row(cat, str(count))

    console.print("\n")
    console.print(table)
    console.print("[bold green]✔ All files organized successfully![/bold green]")


if __name__ == "__main__":
    main()