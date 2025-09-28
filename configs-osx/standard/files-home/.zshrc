# Set up fzf key bindings and fuzzy completion
source <(fzf --zsh)
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
autoload -U colors && colors
HISTFILE=~/.zsh_history
HISTCONTROL=ignoredups:erasedups  # no duplicate entries
HISTSIZE=100000                   # big big history
HISTFILESIZE=100000               # big big history
setopt histappend # append to history, don't overwrite it


PS1="%{$fg[cyan]%}[%*] %{$fg[yellow]%}%~${reset_color}"$'\n'
# PS1="$CYAN\$(date "+%H:%M:%S") $IYELLOW\u:\w\\[\033[\$(parse_git_dirty_color)\]\$(parse_git_repo)\$(__git_ps1)$RESET\n"