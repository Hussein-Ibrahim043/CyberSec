#!/usr/bin/env bash
set -euo pipefail

# install_cybersec.sh
# Run from your project root (the directory that contains CyberSec/)
# Creates ~/bin/cybersec launcher and installs required packages.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$ROOT_DIR/CyberSec"
TOOL_PATH="$PACKAGE_DIR/__init__.py"
LAUNCHER_DIR="$HOME/bin"
LAUNCHER_PATH="$LAUNCHER_DIR/cybersec"
BASHRC="$HOME/.bashrc"
REQ_FILE="$ROOT_DIR/requirements-toolkit.txt"

echo
echo "== Cybersec Toolkit Installer =="
echo "Project root detected: $ROOT_DIR"
echo

# Check package entrypoint
if [ ! -f "$TOOL_PATH" ]; then
  echo "WARNING: Expected toolkit entrypoint not found at:"
  echo "  $TOOL_PATH"
  echo "Make sure the package folder is named 'CyberSec' and contains __init__.py"
  read -p "Continue anyway? (y/N): " yn
  case "$yn" in
    [Yy]*) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

# Create requirements file (third-party libs)
cat > "$REQ_FILE" <<'REQ'
requests
rich
pyfiglet
cryptography
REQ

echo "Created requirements file: $REQ_FILE"
echo

# Check python3 & pip3
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Please install Python 3 and re-run this script." >&2
  exit 1
fi

if ! command -v pip3 >/dev/null 2>&1; then
  echo "pip3 not found — attempting to install pip..."
  python3 -m ensurepip --upgrade || true
fi

# Install packages (user, fallback to system-wide)
echo "Installing Python packages from $REQ_FILE..."
if python3 -m pip install --user -r "$REQ_FILE"; then
  echo "Installed packages to user site-packages."
else
  echo "User install failed, trying system-wide install (sudo may be required)..."
  if command -v sudo >/dev/null 2>&1; then
    sudo python3 -m pip install -r "$REQ_FILE"
  else
    python3 -m pip install -r "$REQ_FILE" || {
      echo "Failed to install packages. Please run this script with sudo or install packages manually." >&2
      exit 1
    }
  fi
fi
echo "Dependencies installed."
echo

# Create ~/bin if needed
if [ ! -d "$LAUNCHER_DIR" ]; then
  mkdir -p "$LAUNCHER_DIR"
  echo "Created $LAUNCHER_DIR"
fi

# Create launcher script
cat > "$LAUNCHER_PATH" <<EOF
#!/usr/bin/env bash
# launcher created by install_cybersec.sh
# Try to run package as module first (recommended), otherwise run __init__.py directly.

# prefer python3 -m CyberSec (works if CyberSec is a package)
if python3 -c "import importlib, sys; importlib.import_module('CyberSec'); sys.exit(0)" 2>/dev/null; then
  exec python3 -m CyberSec "\$@"
else
  exec python3 "$TOOL_PATH" "\$@"
fi
EOF

chmod +x "$LAUNCHER_PATH"
echo "Created launcher: $LAUNCHER_PATH (executable)"

# Ensure ~/bin is in PATH in .bashrc
if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$BASHRC" 2>/dev/null; then
  echo "" >> "$BASHRC"
  echo "# Added by Cybersec Toolkit installer: ensure ~/bin is in PATH" >> "$BASHRC"
  echo 'export PATH="$HOME/bin:$PATH"' >> "$BASHRC"
  echo "Appended PATH update to $BASHRC"
fi

# Add alias 'cybersec' to bashrc if not present
ALIAS_LINE="alias cybersec=\"$LAUNCHER_PATH\""
if ! grep -Fxq "$ALIAS_LINE" "$BASHRC" 2>/dev/null; then
  echo "" >> "$BASHRC"
  echo "# Alias for Cybersec Toolkit" >> "$BASHRC"
  echo "$ALIAS_LINE" >> "$BASHRC"
  echo "Added alias 'cybersec' to $BASHRC"
fi

# Source .bashrc for interactive shells
if [ -n "${PS1-}" ] && [ -f "$BASHRC" ]; then
  # shellcheck disable=SC1090
  source "$BASHRC"
  echo "Sourced $BASHRC (current shell)."
else
  echo "Note: To use the 'cybersec' command in this shell, run: source $BASHRC"
fi

echo
echo "Installation complete!"
echo "You can now run the toolkit with: cybersec"
echo "Or run directly from project root: python3 $TOOL_PATH"
echo "Or run as package: python3 -m CyberSec"
echo
