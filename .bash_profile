# Load ~/.bash_prompt, ~/.exports, ~/.aliases, ~/.functions and ~/.extra
# ~/.extra can be used for settings you don't want to commit
for file in exports aliases extra; do
file="$HOME/.$file"
  [ -e "$file" ] && source "$file"
done

export PROMPT_COMMAND='history -a'
