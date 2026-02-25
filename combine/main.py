import os
import re

# Define the ignore file and the output file.
ignore_file = '.combineignore'
# Output file is a Markdown file.
output_file = "combined_output.md"

def get_language_from_extension(file_path):
    """
    Returns a language identifier for Markdown code blocks based on file extension.
    """
    # Dictionary to map file extensions to language identifiers.
    ext_to_lang = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.json': 'json',
        '.sql': 'sql',
        '.sh': 'shell',
        '.bat': 'batch',
        '.php': 'php',
        '.vue': 'vue',
        '.rb': 'ruby',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.md': 'markdown',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.dockerfile': 'dockerfile',
        'ps1': 'powershell'
    }
    # Get file extension and look it up, return empty string if not found.
    extension = os.path.splitext(file_path)[1].lower()
    return ext_to_lang.get(extension, '')


def get_ignore_patterns(base_dir):
    """
    Reads patterns from .combineignore and converts them into a list of compiled
    regular expressions.
    """
    ignore_patterns = []

    ignore_path = os.path.join(base_dir, ignore_file)
    if os.path.exists(ignore_path):
        print(f"Found '{ignore_file}'. Reading patterns...")
        with open(ignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines.
                if line and not line.startswith('#'):
                    # Convert gitignore patterns to regular expressions.
                    pattern = re.escape(line).replace(r'\*', '.*').replace(r'\?', '.')
                    
                    # Match the entire path or a directory within it.
                    if pattern.endswith('/'):
                        pattern = pattern[:-1] + r'($|/.*)'
                    else:
                        pattern = pattern + r'($|/.*)'
                        
                    ignore_patterns.append(re.compile(f'^{pattern}$'))
    
    return ignore_patterns

def should_ignore(path, base_dir, ignore_patterns):
    """
    Checks if a given path should be ignored based on the compiled patterns.
    """
    rel_path = os.path.relpath(path, base_dir)
    
    # Ignore the output file and the ignore script file itself if found.
    if rel_path == output_file or rel_path == ignore_file:
        return True

    normalized_path = rel_path.replace(os.path.sep, '/')
    
    for pattern in ignore_patterns:
        if pattern.match(normalized_path):
            return True
    return False

# --- Main script ---
base_dir = os.getcwd()

all_ignore_patterns = get_ignore_patterns(base_dir)

with open(output_file, "w", encoding="utf-8") as out:
    # Main title for the combined markdown file for better context.
    out.write("# Combined Directory/Project Files\n\n")

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), base_dir, all_ignore_patterns)]

        for file in files:
            file_path = os.path.join(root, file)
            
            if should_ignore(file_path, base_dir, all_ignore_patterns):
                continue
            
            rel_path = os.path.relpath(file_path, base_dir)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Get language for syntax highlighting
                language = get_language_from_extension(file)

                # --- Writing format to Markdown ---
                # Use a heading for the file path.
                out.write(f"## `{rel_path.replace(os.path.sep, '/')}`\n\n")
                # Use a fenced code block with the detected language.
                out.write(f"```{language}\n")
                out.write(content + "\n")
                out.write("```\n\n")

            except Exception as e:
                print(f"Skipped {file_path}: {e}")

print("="*53)
print(f"Successfully combined files into '{output_file}'")
print("="*53)
