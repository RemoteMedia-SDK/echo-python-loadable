#!/usr/bin/env bash
# Build the plugin cdylib + the host binary, then run the host against
# the freshly-built plugin. Mirrors the shape of
# `examples/loadable-export-smoke/run.sh` for the Python-plugin path.
set -euo pipefail

cd "$(dirname "$0")"

echo "==> Building plugin cdylib (libecho_python_loadable_plugin.so)..."
cargo build

echo "==> Building host..."
(cd host && cargo build)

echo "==> Running host against the freshly-built plugin..."
exec ./host/target/debug/echo-python-loadable-host \
  ./target/debug/libecho_python_loadable_plugin.so
