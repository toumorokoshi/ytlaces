#!/usr/bin/env bash
# Script to build llama.cpp with CUDA support on spark and install binaries to ~/bin

set -ex

SRC_DIR="$HOME/llama.cpp"
BIN_DIR="$HOME/bin"

# Ensure CUDA toolkit paths are set
export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"

echo "=== Preparing llama.cpp source ==="
if [ ! -d "$SRC_DIR" ]; then
    git clone https://github.com/ggml-org/llama.cpp.git "$SRC_DIR"
fi

cd "$SRC_DIR"
# Clean potential dirty states and pull latest
git fetch --all
git reset --hard origin/master

echo "=== Configuring build with CMake ==="
# Enable CUDA backend, and compile statically to avoid shared library lookup issues
cmake -B build -DGGML_CUDA=ON -DBUILD_SHARED_LIBS=OFF

echo "=== Building llama.cpp ==="
cmake --build build --config Release -j$(nproc)

echo "=== Installing binaries to $BIN_DIR ==="
mkdir -p "$BIN_DIR"

# Check if BIN_DIR is owned by the current user. If not, try to fix it using sudo.
if [ "$(stat -c '%u' "$BIN_DIR")" != "$(id -u)" ]; then
    echo "Warning: $BIN_DIR is not owned by the current user (uid: $(id -u))."
    echo "Attempting to fix ownership of $BIN_DIR using sudo..."
    sudo chown -R "$(id -u):$(id -g)" "$BIN_DIR"
fi

# Find and copy all executable binaries from the build/bin directory to ~/bin/
find build/bin -maxdepth 1 -type f -executable -exec cp -v {} "$BIN_DIR/" \;

echo "=== Llama.cpp CUDA build and installation completed successfully! ==="
