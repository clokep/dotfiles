To bootstrap a new computer, some rough steps:

1. Install Firefox, Thunderbird, Bitwarden, Element Nightly
2. [Install homebrew](https://brew.sh/): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3. Install [oh-my-zsh](https://ohmyz.sh/): `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
4. Install homebrew packages `brew bundle --file=Brewfile`
5. Symlink the dotfiles: `python bootstrap.py`
6. Copy history over: `cat .zsh_history.old .zsh_history > tmp; mv tmp .zsh_history`
7. Copy SSH keys
8. Copy documents
9. Increase number of open files: `ulimit -n 1024`
10. Install poetry: `pipx install poetry`
11. Apply macOS customizations: `source .osx`
12. [Install rust](https://rust-lang.org/tools/install/): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

Put any local overrides in a `.extra` file