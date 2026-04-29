# Homebrew initialization (must come before other tools)
if command -v /opt/homebrew/bin/brew &> /dev/null; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Setting PATH for Python 3.11
# The original version is saved in .zprofile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:${PATH}"
export PATH

# Added by OrbStack: command-line tools and integration
# This won't be added again if you remove it.
source ~/.orbstack/shell/init.zsh 2>/dev/null || :

# Added by `rbenv init` on 2026年 2月 8日 星期日 11时45分50秒 CST
eval "$(rbenv init - --no-rehash zsh)"
