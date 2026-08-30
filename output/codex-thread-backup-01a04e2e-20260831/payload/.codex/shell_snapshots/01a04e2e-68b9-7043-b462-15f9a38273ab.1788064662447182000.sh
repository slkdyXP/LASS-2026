# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions

# setopts 2
setopt nohashdirs
setopt login

# aliases 2
alias run-help=man
alias which-command=whence

# exports 24
export CODEX_INTERNAL_ORIGINATOR_OVERRIDE='Codex Desktop'
export CODEX_SHELL=1
export COMMAND_MODE=unix2003
export DISABLE_AUTO_UPDATE=true
export -T FPATH fpath=( /opt/homebrew/share/zsh/site-functions /opt/homebrew/share/zsh/site-functions /usr/local/share/zsh/site-functions /usr/share/zsh/site-functions /usr/share/zsh/5.9/functions )
export HOME=/Users/tanghaohan
export HOMEBREW_CELLAR=/opt/homebrew/Cellar
export HOMEBREW_PREFIX=/opt/homebrew
export HOMEBREW_REPOSITORY=/opt/homebrew
export INFOPATH=/opt/homebrew/share/info:/opt/homebrew/share/info:
export LOGNAME=tanghaohan
export LOG_FORMAT=json
export MallocNanoZone=0
export -T PATH path=( /Applications/ChatGPT.app/Contents/Resources /opt/homebrew/bin /opt/homebrew/sbin /Users/tanghaohan/.local/bin /usr/local/bin /System/Cryptexes/App/usr/bin /usr/bin /bin /usr/sbin /sbin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin /var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin /Library/TeX/texbin /Users/tanghaohan/.codex/tmp/arg0/codex-arg0TqY860 /Users/tanghaohan/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override /Applications/ChatGPT.app/Contents/Resources /Users/tanghaohan/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback )
export RUST_LOG=warn
export SHELL=/bin/zsh
export SSH_AUTH_SOCK=/private/tmp/com.apple.launchd.gE0dVqIU0Y/Listeners
export TMPDIR=/var/folders/y3/drj8bws97cz0yw0ptk5hvj2c0000gn/T/
export USER=tanghaohan
export XPC_FLAGS=0x0
export XPC_SERVICE_NAME=0
export ZSH_TMUX_AUTOSTART=false
export ZSH_TMUX_AUTOSTARTED=true
export __CF_USER_TEXT_ENCODING=0x1F5:0x19:0x34
