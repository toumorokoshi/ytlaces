if status is-interactive
    # Commands to run in interactive sessions can go here
end



set -U fish_greeting ""

fish_add_path $HOME/bin
fish_add_path $HOME/.local/bin
# add rust paths
fish_add_path $HOME/.cargo/bin
# add go paths
fish_add_path /usr/local/go/bin
fish_add_path $HOME/go/bin

function fish_prompt
    set -l last_status $status
    set stat (set_color red)"[$last_status]"(set_color normal)
    set curDate (set_color cyan)(/usr/bin/date "+%H:%M:%S")(set_color normal)
    set curDir (set_color green)$PWD(set_color normal)
    set gitBranch (set_color yellow)\((/usr/bin/git branch --show-current 2>/dev/null)\) (set_color normal)
    printf "$stat $curDate $curDir $gitBranch"
    echo
end

# bind alt+f to accept a completion suggestion
# bind alt+f accept-completion
bind -M default --user shift-enter accept-autosuggestion

tome init s ~/.ytlaces/cookbook "fish" | source

# install fisher extensions
# curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
# fisher install jethrokuan/fzf
