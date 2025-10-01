#!/usr/bin/env bash
set -euo pipefail

# install_cybersec.sh
# Run this from inside CyberSec/ directory
# - Creates a .venv in project root (CyberSec/.venv)
# - Installs required packages
# - Creates ~/bin/cybersec launcher
# - Adds PATH + alias to the current user's ~/.bashrc and ~/.zshrc

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$ROOT_DIR"
TOOL_PATH="$PACKAGE_DIR/__init__.py"
LAUNCHER_DIR="$HOME/bin"
LAUNCHER_PATH="$LAUNCHER_DIR/cybersec"
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"
REQ_FILE="$ROOT_DIR/requirements-toolkit.txt"
VENV_DIR="$ROOT_DIR/.venv"

# Colors for pretty printing
GREEN="\033[92m"
CYAN="\033[1;36m"
YELLOW="\033[93m"
MAGENTA="\033[95m"
RESET="\033[0m"

echo
echo -e "${CYAN}== CyberSec Toolkit Installer ==${RESET}"
echo "Project root: $ROOT_DIR"
echo

# Check entrypoint
if [ ! -f "$TOOL_PATH" ]; then
  echo -e "${YELLOW}WARNING:${RESET} __init__.py not found at:"
  echo "  $TOOL_PATH"
  echo "If your entrypoint differs, adjust TOOL_PATH in this script."
  read -p "Continue anyway? (y/N): " yn
  case "$yn" in
    [Yy]*) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

# Create requirements file
cat > "$REQ_FILE" <<'REQ'
requests
rich
pyfiglet
cryptography
REQ
echo -e "${GREEN}Created requirements file: $REQ_FILE${RESET}"

# Check python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Please install it and re-run." >&2
  exit 1
fi

# Create venv
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi

# Install packages
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$REQ_FILE"
deactivate
echo -e "${GREEN}Dependencies installed in $VENV_DIR.${RESET}"

# Create ~/bin if missing
mkdir -p "$LAUNCHER_DIR"

# Create launcher
cat > "$LAUNCHER_PATH" <<LAUNCHER
#!/usr/bin/env bash
VENV_DIR="$VENV_DIR"
TOOL_PY="$TOOL_PATH"
PY="\$VENV_DIR/bin/python"

if "\$PY" -c "import CyberSec" 2>/dev/null; then
  exec "\$PY" -m CyberSec "\$@"
elif [ -f "\$TOOL_PY" ]; then
  exec "\$PY" "\$TOOL_PY" "\$@"
else
  echo "ERROR: Cannot run CyberSec (module not found, no __init__.py)"
  exit 2
fi
LAUNCHER

chmod +x "$LAUNCHER_PATH"
echo -e "${GREEN}Created launcher at $LAUNCHER_PATH${RESET}"

# Add alias + PATH to rc files
add_rc_entries() {
  local rcfile="$1"
  local rcname="$2"

  local path_line='export PATH="$HOME/bin:$PATH"'
  local alias_line="alias cybersec=\"$LAUNCHER_PATH\""

  [ ! -f "$rcfile" ] && touch "$rcfile"

  grep -qF "$path_line" "$rcfile" || {
    echo "" >> "$rcfile"
    echo "# Added by CyberSec installer" >> "$rcfile"
    echo "$path_line" >> "$rcfile"
    echo -e "${CYAN}Updated PATH in $rcname${RESET}"
  }

  grep -qF "$alias_line" "$rcfile" || {
    echo "" >> "$rcfile"
    echo "# CyberSec alias" >> "$rcfile"
    echo "$alias_line" >> "$rcfile"
    echo -e "${CYAN}Added alias to $rcname${RESET}"
  }
}

add_rc_entries "$BASHRC" "bashrc"
add_rc_entries "$ZSHRC" "zshrc"   # <-- always user’s ~/.zshrc

# Source rc file in current shell if possible
if [ -n "${PS1-}" ]; then
  case "$(basename "${SHELL:-}")" in
    zsh) [ -f "$ZSHRC" ] && source "$ZSHRC" ;;
    bash) [ -f "$BASHRC" ] && source "$BASHRC" ;;
  esac
fi

echo
echo -e "${GREEN}[+] Installation complete!${RESET}"
echo -e "${MAGENTA}Run with: cybersec${RESET}"
echo -e "${MAGENTA}Or directly: $VENV_DIR/bin/python $TOOL_PATH${RESET}"
