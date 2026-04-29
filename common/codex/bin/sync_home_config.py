#!/usr/bin/env python3
"""将仓库中的 Codex 模板配置同步到 ~/.codex/config.toml。

设计目标：
1. `~/.codex/config.toml` 保持为普通文件，避免 Codex 原子写回时覆盖软链接。
2. 仓库里的模板继续作为模型、MCP、UI 等“受管默认值”的来源。
3. 用户运行过程中产生的动态状态（如项目信任列表）保留在 `~/.codex/config.toml`。
"""

from __future__ import annotations

import copy
import json
import re
import tomllib
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / ".codex" / "config.toml"
TARGET_PATH = Path.home() / ".codex" / "config.toml"

RUNTIME_PRESERVED_KEYS = {
    "projects",
    "mcp_servers",
}

_BARE_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def load_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("rb") as file:
        data = tomllib.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"{path} 的 TOML 根节点不是 table")

    return data


def merge_configs(template: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    """按“模板兜底 + 运行时状态保留”的策略合并配置。"""

    merged = copy.deepcopy(current)

    for key, value in template.items():
        if key in RUNTIME_PRESERVED_KEYS:
            continue
        merged[key] = copy.deepcopy(value)

    merged_projects = copy.deepcopy(template.get("projects", {}))
    for project_path, project_config in current.get("projects", {}).items():
        merged_projects[project_path] = copy.deepcopy(project_config)
    if merged_projects:
        merged["projects"] = merged_projects

    merged_mcp_servers = copy.deepcopy(current.get("mcp_servers", {}))
    template_server_names = set(template.get("mcp_servers", {}).keys())

    # 允许模板明确下线已受管的 MCP。
    for server_name in list(merged_mcp_servers.keys()):
        if server_name == "aivectormemory" and server_name not in template_server_names:
            merged_mcp_servers.pop(server_name, None)

    for server_name, server_config in template.get("mcp_servers", {}).items():
        merged_mcp_servers[server_name] = copy.deepcopy(server_config)
    if merged_mcp_servers:
        merged["mcp_servers"] = merged_mcp_servers

    return merged


def format_key(key: str) -> str:
    if _BARE_KEY_PATTERN.match(key):
        return key
    return json.dumps(key, ensure_ascii=False)


def format_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, list):
        if any(isinstance(item, dict) for item in value):
            raise TypeError("array-of-tables 需要走专用写出逻辑")
        return "[" + ", ".join(format_value(item) for item in value) + "]"

    value_type = type(value).__name__
    raise TypeError(f"暂不支持写出 {value_type} 类型到 TOML")


def is_array_of_tables(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, dict) for item in value)


def split_table_items(
    table: dict[str, Any],
) -> tuple[list[tuple[str, Any]], list[tuple[str, dict[str, Any]]], list[tuple[str, list[dict[str, Any]]]]]:
    scalar_items: list[tuple[str, Any]] = []
    nested_items: list[tuple[str, dict[str, Any]]] = []
    array_table_items: list[tuple[str, list[dict[str, Any]]]] = []

    for key, value in table.items():
        if isinstance(value, dict):
            nested_items.append((key, value))
        elif is_array_of_tables(value):
            array_table_items.append((key, value))
        else:
            scalar_items.append((key, value))

    return scalar_items, nested_items, array_table_items


def emit_array_table(lines: list[str], path: list[str], table: dict[str, Any]) -> None:
    scalar_items, nested_items, array_table_items = split_table_items(table)
    section_name = ".".join(format_key(part) for part in path)
    lines.append(f"[[{section_name}]]")

    for key, value in scalar_items:
        lines.append(f"{format_key(key)} = {format_value(value)}")

    for key, value in nested_items:
        if lines and lines[-1] != "":
            lines.append("")
        emit_table(lines, [*path, key], value)

    for key, value in array_table_items:
        for item in value:
            if lines and lines[-1] != "":
                lines.append("")
            emit_array_table(lines, [*path, key], item)


def emit_table(lines: list[str], path: list[str], table: dict[str, Any]) -> None:
    scalar_items, nested_items, array_table_items = split_table_items(table)

    if path and scalar_items:
        section_name = ".".join(format_key(part) for part in path)
        lines.append(f"[{section_name}]")

    for key, value in scalar_items:
        lines.append(f"{format_key(key)} = {format_value(value)}")

    for key, value in nested_items:
        if lines and lines[-1] != "":
            lines.append("")
        emit_table(lines, [*path, key], value)

    for key, value in array_table_items:
        for item in value:
            if lines and lines[-1] != "":
                lines.append("")
            emit_array_table(lines, [*path, key], item)


def dumps_toml(data: dict[str, Any]) -> str:
    lines = [
        "# 此文件由 ~/.dotfiles/common/codex/bin/sync_home_config.py 同步生成。",
        "# 请把共享默认配置改在 ~/.dotfiles/common/codex/.codex/config.toml，",
        "# 运行时状态（如项目信任列表）则保留在 ~/.codex/config.toml。",
        "",
    ]

    root_scalars: dict[str, Any] = {}
    root_tables: dict[str, dict[str, Any]] = {}
    root_array_tables: dict[str, list[dict[str, Any]]] = {}
    for key, value in data.items():
        if isinstance(value, dict):
            root_tables[key] = value
        elif is_array_of_tables(value):
            root_array_tables[key] = value
        else:
            root_scalars[key] = value

    for key, value in root_scalars.items():
        lines.append(f"{format_key(key)} = {format_value(value)}")

    for key, value in root_tables.items():
        if lines and lines[-1] != "":
            lines.append("")
        emit_table(lines, [key], value)

    for key, value in root_array_tables.items():
        for item in value:
            if lines and lines[-1] != "":
                lines.append("")
            emit_array_table(lines, [key], item)

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    template = load_toml(TEMPLATE_PATH)
    current = load_toml(TARGET_PATH)

    merged = merge_configs(template, current)
    rendered = dumps_toml(merged)

    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if TARGET_PATH.exists() and TARGET_PATH.read_text(encoding="utf-8") == rendered:
        return 0

    TARGET_PATH.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
