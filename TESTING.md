# Running Tests for pyxconfig Project

## Overview

This document provides instructions on how to run the unit tests for the pyxconfig project. The tests ensure that the various functions within the `pyxconfig.py` script work correctly.

## Prerequisites

1. **Python 3.x**: Ensure that Python 3.x is installed on your system. You can check the installed version by running:

```
   python3 --version
```

    unittest module: The unittest module is included in the standard Python library, so no additional installation is necessary.

## Directory Structure

Ensure that your directory structure looks like this:

```
pyxconfig/
├── cardDetect/
│   ├── XF86Config.amd
│   ├── XF86Config.intel
│   ├── XF86Config.nvidia
│   ├── XF86Config.nvidia-hybrid
│   ├── XF86Config.radeon
│   ├── XF86Config.scfb
│   ├── XF86Config.vesa
│   ├── XF86Config.virtualbox
│   └── XF86Config.vmware
├── config/
│   ├── nvidia_304.txt
│   ├── nvidia_340.txt
│   ├── nvidia_390.txt
│   ├── nvidia_470.txt
│   ├── nvidia_latest.txt
│   └── radeon_devices.txt
├── scripts/
│   └── pyxconfig.py
├── tests/
│   └── test_pyxconfig.py
├── pyxconfig.json
├── LICENSE
├── README.md
└── TESTING.md
```

## Running the Tests

    Navigate to the Project Directory: Open a terminal and navigate to the root directory of the project:

```
cd path/to/pyxconfig
```

Run the Tests: Use the unittest module to discover and run the tests:

```
    python3 -m unittest discover tests
```

    This command will automatically discover all test files in the tests directory and execute them.

## Understanding Test Results
```
    OK: Indicates that all tests passed successfully.
    FAIL: Indicates that one or more tests failed. The output will show which tests failed and the reasons for the failure.
    ERROR: Indicates that there was an error in the test execution itself. This usually points to an issue in the test setup.
```
Example Output

Here is an example of what the test output might look like:

```
$ python3 -m unittest discover tests
..........
----------------------------------------------------------------------
Ran 10 tests in 0.005s

OK
```
In this example, all tests passed, as indicated by the OK status.
Adding New Tests

To add new tests, create a new Python file in the tests directory and define your test cases using the unittest module. Ensure your test file name starts with test_ to be automatically discovered by the unittest module.

## Further Reading

    unittest Documentation

This guide should help you effectively run and manage tests for the pyxconfig project.

