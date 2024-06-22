# pyxconfig Project

## Overview

This project provides a script to configure graphics drivers on a FreeBSD or GhostBSD system. The script detects the installed graphics card and sets up the appropriate driver.

## Directory Structure

```
pyxconfig/
├── cardDetect/
│ ├── XF86Config.amd
│ ├── XF86Config.intel
│ ├── XF86Config.nvidia
│ ├── XF86Config.nvidia-hybrid
│ ├── XF86Config.radeon
│ ├── XF86Config.scfb
│ ├── XF86Config.vesa
│ ├── XF86Config.virtualbox
│ └── XF86Config.vmware
├── config/
│ ├── nvidia_304.txt
│ ├── nvidia_340.txt
│ ├── nvidia_390.txt
│ ├── nvidia_470.txt
│ ├── nvidia_latest.txt
│ └── radeon_devices.txt
├── scripts/
│ └── pyxconfig.py
├── tests/
│ └── test_pyxconfig.py
├── pyxconfig.json
├── LICENSE
├── README.md
└── TESTING.md
```

## Configuration

### `pyxconfig.json`

This file contains the paths to the device files. Example content:
```
{
  "nvidia_device_files": {
    "latest": "config/nvidia_latest.txt",
    "470": "config/nvidia_470.txt",
    "390": "config/nvidia_390.txt",
    "340": "config/nvidia_340.txt",
    "304": "config/nvidia_304.txt"
  },
  "radeon_device_file": "config/radeon_devices.txt",
  "card_detect_directory": "cardDetect/"
}
```

## Usage

    Ensure you have the necessary dependencies installed.
    Run the script as the root user:

```
python3 scripts/pyxconfig.py <setup|auto>
```

## License

This project is licensed under the BSD 2-Clause "Simplified" License.

