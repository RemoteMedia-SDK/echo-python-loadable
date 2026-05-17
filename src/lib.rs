//! Echo-only Python plugin — smallest possible
//! [`python_plugin_export!`] proof point.
//!
//! Mirrors the shape of [`examples/loadable-export-smoke/`] (Rust-side
//! dual-emit smoke test) for the Python-plugin path. Bundles a single
//! `EchoPythonNode` Python class (no ML deps) into a cdylib and
//! registers it under `node_type = "EchoPythonNode"`.
//!
//! What this validates today:
//! - `include_dir!` embedding survives `cargo build --release`.
//! - `python_plugin_export!` macro expands cleanly.
//! - The host's `LoadableNodeBundle::load()` can dlopen the resulting
//!   `.so` and surface the factory through abi_stable.
//!
//! What's pending (Task 3.3.3-3.3.6 in
//! `openspec/changes/add-loadable-python-nodes/tasks.md`):
//! - Factory `create()` currently returns a precise RErr — venv
//!   provisioning + subprocess + iceoryx2 wiring lands next.
//! - End-to-end "send text, get echo back" round-trip.

use include_dir::{include_dir, Dir};

// Embedded Python source tree. Resolved at compile time relative to
// `$CARGO_MANIFEST_DIR`. Build fails (loudly) if the directory is
// missing — exactly the fail-fast behaviour we want.
static EMBED: Dir<'_> = include_dir!("$CARGO_MANIFEST_DIR/embedded");

remotemedia_plugin_sdk::python_plugin_export! {
    node_type: "EchoPythonNode",
    module:    "echo_python",
    class:     "EchoPythonNode",
    embedded:  &EMBED,
}
