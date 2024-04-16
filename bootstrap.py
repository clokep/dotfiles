#!/usr/bin/env python 

# Basic Imports
import os
import sys

# Global - add files you want to ignore in the current directory
IGNORED_FILES = [".gitignore", "bootstrap.py", "README.md", "LICENSE"]

if __name__ == "__main__":
    """
    Run this out of the .dotfiles directory to symlink the appropriate
    files into your home directory
    """

    current_directory = os.getcwd()
    home = os.getenv("HOME")

    if not current_directory.endswith("dotfiles"):
        print("Are you running this outside of the dotfiles directory?")
        sys.exit(1)

    else:
        dotfiles  = os.listdir(current_directory)

        for f in dotfiles:
            if f.endswith("~") or os.path.isdir(f) or (f in IGNORED_FILES):
                print(f"Ignoring temp file or directory: {f}")
                continue
            
            elif f.startswith("."):
                original = current_directory + "/" + f
                home_file = home + "/" + f
                print(f"Linking: {original} --> {home_file}")
                os.system(f"ln -si {original} {home_file}")

            else:
                print("We encountered some weird file and are ignoring it")

    print("Done linking...")
