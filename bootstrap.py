#!/usr/bin/env python 

import os
import sys

from pathlib import Path

# Files to ignore in the root directory.
IGNORED_FILES = {".git", ".gitignore", ".idea", ".osx", "bootstrap.py", "Brewfile", "LICENSE", "README.md"}

def symlink_path(current_directory: Path, current_home: Path, ignored_files: set[str] = set()) -> None:
    files = sorted(current_directory.iterdir())

    for f in files:
        if f.name.endswith("~") or (f.name in ignored_files):
            print(f"Ignoring: {f}")
            continue

        if f.is_dir():
            new_target = current_home / f.name
            if not new_target.exists():
                new_target.mkdir()
            elif not new_target.is_dir():
                print(f"Sub-directory path exists and is not a directory: {new_target}")
                continue

            symlink_path(f, current_home / f.name)
            continue

        else:
            home_file = current_home / f.name

            # If file exists and points to the right spot, all good.
            if home_file.resolve() == f:
                print(f"Already linked: {f}")

            # If file exists and doesn't point to the right spot, we need a human.
            elif home_file.exists():
                print(f"Already exists: {f}")

            # Otherwise, link the file.
            else:
                print(f"Linking:  {home_file} --> {f}")
                home_file.symlink_to(f)


if __name__ == "__main__":
    """
    Run this out of the .dotfiles directory to symlink the appropriate
    files into your home directory
    """

    working_dir = Path(__file__).parent
    home = Path(os.getenv("HOME"))

    if working_dir.name != "dotfiles":
        print("Are you running this outside of the dotfiles directory?")
        sys.exit(1)

    symlink_path(working_dir, home, IGNORED_FILES)

    print("Done linking...")
