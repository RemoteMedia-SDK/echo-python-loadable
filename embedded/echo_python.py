# /// script
# dependencies = []
# ///

"""Trivial Python echo node for the python_plugin_export! smoke example.

Prepended-to-input echo: every text input comes back as
``"echo: <text>"``. Zero ML deps — validates the loadable-plugin
distribution path (cdylib + embedded Python + venv provisioning + runner
spawn) without dragging torch/transformers into the example.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncGenerator

try:
    from remotemedia.core.multiprocessing.data import RuntimeData
    _HAS_RUNTIME_DATA = True
except ImportError:
    _HAS_RUNTIME_DATA = False
    RuntimeData = None  # type: ignore

from remotemedia.core.multiprocessing import (
    MultiprocessNode,
    NodeConfig,
    python_requires,
    register_node,
)

logger = logging.getLogger(__name__)


@register_node("EchoPythonNode")
@python_requires([])  # No external Python deps — runner-only.
class EchoPythonNode(MultiprocessNode):
    """Echo every text input back, prefixed with ``"echo: "``.

    Exercises the loadable-plugin distribution machinery (cdylib embed,
    extraction, venv provisioning, runner spawn) without ML weight.
    """

    def __init__(
        self,
        config: NodeConfig | dict | str | None = None,
        **kwargs: Any,
    ) -> None:
        # The multiprocess runner currently invokes node classes as
        # `node_class(self.config.node_id)` — see runner.py:233.
        # That hands us a bare string positional. Normalize all four
        # input shapes (None / str / dict / NodeConfig) into a real
        # NodeConfig before passing to the parent.
        if isinstance(config, str):
            config = NodeConfig(
                node_id=config,
                node_type="EchoPythonNode",
                params={},
            )
        elif config is None:
            config = NodeConfig(
                node_id="echo_python",
                node_type="EchoPythonNode",
                params={},
            )
        elif isinstance(config, dict):
            config = NodeConfig(
                node_id=config.get("node_id", "echo_python"),
                node_type=config.get("node_type", "EchoPythonNode"),
                params=config.get("params", {}),
            )
        super().__init__(config, **kwargs)
        self.is_streaming = True

    async def initialize(self) -> None:
        logger.info("[%s] EchoPythonNode ready", self.node_id)

    async def cleanup(self) -> None:
        logger.info("[%s] EchoPythonNode cleaned up", self.node_id)

    async def process(self, data: Any) -> AsyncGenerator[Any, None]:
        if not _HAS_RUNTIME_DATA or RuntimeData is None:
            logger.error("[%s] RuntimeData bindings unavailable", self.node_id)
            return

        text: str
        if hasattr(data, "is_text") and data.is_text():
            text = data.as_text()
        elif isinstance(data, str):
            text = data
        else:
            kind = getattr(data, "data_type", lambda: type(data).__name__)()
            text = f"<non-text:{kind}>"

        yield RuntimeData.text(f"echo: {text}")


# Full-path registry alias — mirrors the moss_tts_realtime.py pattern so
# the FFI runner can resolve `EchoPythonNode` by either bare or full name.
try:
    from remotemedia.core.multiprocessing import _NODE_REGISTRY as _MP_REGISTRY
    _MP_REGISTRY[f"{EchoPythonNode.__module__}.{EchoPythonNode.__name__}"] = EchoPythonNode
except ImportError:
    pass
