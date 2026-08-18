#!/usr/bin/env python 

import os
import sys

from pathlib import Path

# Global - add files you want to ignore in the current directory
IGNORED_FILES = [".gitignore", ".osx", "bootstrap.py", "README.md", "LICENSE", "Brewfile"]

if __name__ == "__main__":
    """
    Run this out of the .dotfiles directory to symlink the appropriate
    files into your home directory
    """

    current_directory = Path(__file__).parent
    home = Path(os.getenv("HOME"))

    if current_directory.name != "dotfiles":
        print("Are you running this outside of the dotfiles directory?")
        sys.exit(1)

    else:
        files  = sorted(current_directory.glob(".*"))

        for f in files:
            if f.name.endswith("~") or f.is_dir() or (f.name in IGNORED_FILES):
                print(f"Ignoring: {f}")
                continue
            
            elif f.name.startswith("."):
                home_file = home / f.name

                # If file exists and points to the right spot, all good.
                if home_file.resolve() == f:
                    print(f"Ignoring: {f}")

                # If file exists and doesn't point to the right spot, we need a human.
                elif home_file.exists():
                    print(f"Already exists: {f}")

                # Otherwise, link the file.
                else:
                    print(f"Linking:  {home_file} --> {f}")
                    home_file.symlink_to(f)

            else:
                # This should never happen due to the glob.
                print("We encountered some weird file and are ignoring it")

    print("Done linking...")
