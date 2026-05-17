# echo-python-loadable — minimum-viable Path 4 Python plugin

Smallest possible Python-plugin proof point. Rust cdylib that embeds
a single `echo_python.py` (no ML deps, single class, just round-trips
text) via `include_dir!` and registers `EchoPythonNode` into the SDK
registry.

Sister to:

- [`RemoteMedia-SDK/echo-python-source`](https://github.com/RemoteMedia-SDK/echo-python-source)
  — same node, shipped as Path 5 (`plugin.toml` + `.py` only, no Rust).
- [`RemoteMedia-SDK/moss-tts-realtime`](https://github.com/RemoteMedia-SDK/moss-tts-realtime)
  — canonical heavy Path 4 plugin with vendored sub-package + ML deps.

## Use from a manifest

```json
{
  "version": "v1",
  "plugins": ["echo-python-loadable@v0.1.0"],
  "nodes": [
    { "id": "echo", "node_type": "EchoPythonNode", "params": {} }
  ]
}
```

The SDK resolver expands `echo-python-loadable@v0.1.0` to
`github.com/RemoteMedia-SDK/echo-python-loadable`, fetches
`plugin.toml`, then falls through to `release-manifest.json` for the
platform-specific prebuilt `.so` / `.dylib` / `.dll` asset.

> **Status:** plugin.toml + source published. **Prebuilt release
> binaries are not yet uploaded** — the matrix-build CI workflow is
> pending. Until then, consumers should either build the cdylib
> themselves (see below) or use a local-path plugin entry.

## Build the cdylib locally

```bash
git clone https://github.com/RemoteMedia-SDK/echo-python-loadable
cd echo-python-loadable
cargo build --release
# → target/release/libecho_python_loadable_plugin.so
```

Then reference it from your manifest:

```json
{ "plugins": ["./path/to/libecho_python_loadable_plugin.so"] }
```

## What it exports

| Node type        | Input | Output           |
|------------------|-------|------------------|
| `EchoPythonNode` | Text  | Text (`"echo: " + input`) |

## What's in the repo

```
echo-python-loadable/
├── plugin.toml             ← metadata
├── Cargo.toml              ← git-deps the SDK at a pinned rev
├── src/lib.rs              ← `python_plugin_export!{...}` macro call
├── embedded/echo_python.py ← the actual node implementation
├── run.sh                  ← local smoke-test driver
└── README.md
```

## Compare to the source-load path

| Aspect | `echo-python-loadable` (this repo, Path 4) | [`echo-python-source`](https://github.com/RemoteMedia-SDK/echo-python-source) (Path 5) |
|---|---|---|
| Languages plugin author writes | Rust + Python | **Python only** |
| Build step | `cargo build` per platform | None |
| Distribution | `.so` / `.dylib` / `.dll` (matrix per OS+arch) | git tag |
| Source visible to consumer | No (embedded in binary) | Yes (cloned) |
| First-load time | Fast (dlopen) | Slower (tarball download + extract + venv) |

## License

See `LICENSE.md`. This plugin reuses RemoteMedia SDK source and is
governed by the same RemoteMedia SDK Community License 1.0.
