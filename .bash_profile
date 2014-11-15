# Load ~/.bash_prompt, ~/.exports, ~/.aliases, ~/.functions and ~/.extra
# ~/.extra can be used for settings you don’t want to commit
for file in exports aliases extra; do
file="$HOME/.$file"
  [ -e "$file" ] && source "$file"
done

################### Start History Control ########################
export HISTCONTROL=ignoredups
export HISTCONTROL=ignoreboth
export HISTTIMEFORMAT='%Y-%m-%d %H:%M:%S '
export HISTFILESIZE=2000
export HISTIGNORE="[ ]*:&:bg:fg:exit" # Ignore some controlling instructions
#setopt -s histappend # Make bash append rather than overwrite the history on disk
#setopt -s cmdhist # save multiple line commands to a single history line
#export PROMPT_COMMAND="history -a; history -c; history -r"
export PROMPT_COMMAND='history -a'
################### End History Control ########################

# Case-insensitive globbing (used in pathname expansion)
#setopt -s nocaseglob

# Add tab completion for SSH hostnames based on ~/.ssh/config, ignoring wildcards
#[ -e "$HOME/.ssh/config" ] && complete -o "default" -o "nospace" -W "$(grep "^Host" ~/.ssh/config | grep -v "[?*]" | cut -d " " -f2)" scp sftp ssh

if [ -e .git-completion.bash ]; then source .git-completion.bash; fi
if [ -e "$HOME/.work-env" ]; then source $HOME/.work-env; fi
