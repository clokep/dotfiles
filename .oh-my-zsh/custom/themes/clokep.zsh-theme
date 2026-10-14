PROMPT="%{$fg[cyan]%}%c%{$reset_color%}"
PROMPT+=' $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}%1{✗%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"

# Last command runtime (yellow > 5s, red > 30s) and a clock colored by exit status.
zmodload zsh/datetime
autoload -Uz add-zsh-hook

_preexec() {
  _cmd_start=$EPOCHSECONDS
}

_precmd() {
  _cmd_elapsed=""
  if [[ -n $_cmd_start ]]; then
    local elapsed=$(( EPOCHSECONDS - _cmd_start ))
    if (( elapsed > 30 )); then
      _cmd_elapsed="%F{red}${elapsed}s%f "
    elif (( elapsed > 5 )); then
      _cmd_elapsed="%F{yellow}${elapsed}s%f "
    fi
    unset _cmd_start
  fi
}

add-zsh-hook preexec _preexec
add-zsh-hook precmd _precmd

RPROMPT='${_cmd_elapsed}%(?.%F{green}.%F{red})%*%f'
