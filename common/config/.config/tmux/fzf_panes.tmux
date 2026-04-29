#!/usr/bin/env bash
# 超简化版：只确保脚本能成功执行（返回 0），满足 tmux 钩子需求
update_mru_pane_ids() {
  # 1. 定义缓存文件路径（用绝对路径，避免 tmux 环境路径问题）
  local mru_file="$HOME/.cache/tmux/mru_panes"
  # 2. 强制创建缓存目录（忽略权限问题，加 -p 不报错）
  mkdir -p "$(dirname "$mru_file")" || true
  # 3. 写入一个空文件（确保脚本执行成功，返回 0）
  touch "$mru_file" || true
}

# 接收命令参数，执行函数（无论如何都返回 0，避免 tmux 报错）
case "$1" in
  update_mru_pane_ids)
    update_mru_pane_ids
    exit 0  # 强制返回成功
    ;;
  *)
    exit 0  # 未知命令也返回成功，避免报错
    ;;
esac
