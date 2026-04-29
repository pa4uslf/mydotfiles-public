PS1="\w bash >" # 修改bash命令提示符

# 新增：一些常用别名
alias ll='ls -lah'
alias gs='git status'

# Agent Reach / mcporter:
# 默认把 mcporter 的配置固定到 ~/.agent-reach/config/mcporter.json，
# 这样无论当前在哪个目录，都会使用同一套 MCP 配置。
# 如果你明确传入 --config，则尊重手动指定的配置文件。
mcporter() {
    local agent_reach_root="${AGENT_REACH_ROOT:-$HOME/.agent-reach}"
    local mcporter_config="$agent_reach_root/config/mcporter.json"

    if [ "$1" = "--config" ]; then
        command mcporter "$@"
    else
        command mcporter --config "$mcporter_config" "$@"
    fi
}

[ ! -f "$HOME/.x-cmd.root/X" ] || . "$HOME/.x-cmd.root/X" # boot up x-cmd.
. "$HOME/.cargo/env"

# Added by LM Studio CLI tool (lms)
export PATH="$PATH:$HOME/.lmstudio/bin"
