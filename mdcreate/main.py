import argparse
import os
import re
import sys


def recreate_files_from_markdown(md_file, output_dir="."):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match sections like: ## `path/to/file`
    pattern = re.compile(
        r"## `([^`]+)`\s+```[a-zA-Z0-9]*\n(.*?)```",
        re.S
    )

    matches = pattern.findall(content)
    if not matches:
        print("No files found in markdown.")
        return

    for filepath, filecontent in matches:
        full_path = os.path.join(output_dir, filepath)

        # Ensure directories exist
        directory = os.path.dirname(full_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(full_path, "w", encoding="utf-8", newline="") as f:
            f.write(filecontent.strip() + "\n")

        print(f"Created: {full_path}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Recreate files from a combined markdown file."
    )

    parser.add_argument(
        "markdown_file",
        nargs="?",
        default="combined_output.md",
        help="Markdown file to extract from (default: combined_output.md)"
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        default="extracted_project",
        help="Directory where files will be created (default: extracted_project)"
    )

    args = parser.parse_args()

    if not args.markdown_file.lower().endswith(".md"):
        parser.error("Input file must have a .md extension.")

    if not os.path.isfile(args.markdown_file):
        parser.error(f"File not found: {args.markdown_file}")

    return args


if __name__ == "__main__":
    args = parse_args()

    recreate_files_from_markdown(
        args.markdown_file,
        output_dir=args.output_dir
    )