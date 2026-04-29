# mydotfiles-public

Public-safe subset of my local dotfiles.

This repository is generated from a private dotfiles repository with a whitelist
export script. It intentionally excludes machine-specific, private, and
high-trust automation files.

## Included

- Bash, inputrc, tmux, Vim, zprofile, curl, and gem configuration.
- Public-safe Git ignore configuration and a sanitized `.gitconfig` template.
- Selected terminal and CLI helper configuration under `common/config`.
- Sanitized Codex workflow docs, prompts, sample config, and reusable helper
  scripts under `common/codex`.
- Public-safe Codex automation, contract-first, harness, and agent role
  configuration templates.
- Stow-compatible directory layout.

## Excluded

- Secrets, tokens, private environment files, and encrypted material.
- Private/work machine packages.
- Backup directories and historical migration artifacts.
- Local Codex runtime config, MCP wrappers, real browser-login automation state,
  and machine-specific trusted project paths.
- LaunchAgents, tunnel notification scripts, backup jobs, and local service
  automation.
- The private `.zshrc`, because it contains local automation and machine
  paths. Add your own zsh profile on top of this public base.
- Memory policy, founder coaching, and marketing routing docs are intentionally
  kept private or should be published only as separate curated guides.

## Install

```bash
brew install stow
git clone https://github.com/pa4uslf/mydotfiles-public.git ~/.dotfiles-public
cd ~/.dotfiles-public
stow -d common -t ~ bashrc curlrc gem git inputrc tmux vim zprofile
```

The exported `common/codex` directory is documentation-first. Review and adapt
`common/codex/.codex/config.example.toml` before using it as a live Codex config.

## Sync From Private Source

This public repository is not edited by hand. From the private dotfiles repo:

```bash
~/.dotfiles/scripts/export-public-dotfiles.sh ~/mydotfiles-public
cd ~/mydotfiles-public
gitleaks detect --source . --no-git --redact
detect-secrets scan --all-files
git status
```

Review the diff before committing and pushing.
