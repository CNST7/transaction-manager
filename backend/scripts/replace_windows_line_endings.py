#!/usr/bin/env python
from pathlib import Path

entrypoint_path = Path(".") / "entrypoint.sh"
entrypoint_data = entrypoint_path.read_bytes()
entrypoint_data_lf = entrypoint_data.replace(b"\r\n", b"\n")
entrypoint_path.write_bytes(entrypoint_data_lf)
