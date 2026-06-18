# Scripts

These scripts are made for my use cases, to simplify my work and cut time to get things done.
Must of them are built with `Python`, and I plan to make `Powershell`, and `Bash` versions of these scripts.

> Note that I got a lot of help building these scripts using AI.

## Combine

Is a simple yet powerful script that combines all files in a specific directory and output them to a markdown `.md` file name `combine_output.md` it can be used for multiple use cases, it reads from a special file `.combineignore` like `.gitignore` file to ignore files and directories and uses the same pattern.

1. Main use case: For AI chat bots, it makes it easy to make the AI read a lot of the codebase and have an inside of what is this directory/project.
1. Secondary use case: to have simple and stupid backup of a directory instead of git, combined with another script in this `Scripts` repo called `mdcreate`.

## mdCreate

Is the repository mentioned in the `Combine` script section that reads a markdown file `.md` based on the `Combine` script layout, and then create a directory of the files contained inside the previous mentioned file.

---

...
