import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
import sys

# Add the scripts directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from pyxconfig import (
    run_command,
    is_root,
    setup_virtualbox,
    install_and_setup_nvidia,
    setup_intel_drm,
    setup_amd_radeonkms_drm,
    setup_amdgpu_radeonkms_drm,
    fail_safe,
    manual_setup,
    auto_configure_x,
    load_config,
    detect_nvidia_driver,
    detect_radeon_device,
    get_driver_from_xdrivers
)

class TestPyxconfig(unittest.TestCase):

    @patch('pyxconfig.subprocess.run')
    def test_run_command_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout='output', returncode=0)
        output = run_command(['echo', 'hello'])
        self.assertEqual(output, 'output')

    @patch('pyxconfig.subprocess.run')
    def test_run_command_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', 'error')
        output = run_command(['false'])
        self.assertIsNone(output)

    @patch('pyxconfig.os.geteuid', return_value=0)
    def test_is_root(self, mock_geteuid):
        self.assertTrue(is_root())

    @patch('pyxconfig.os.geteuid', return_value=1000)
    def test_is_not_root(self, mock_geteuid):
        self.assertFalse(is_root())

    @patch('pyxconfig.run_command')
    def test_setup_virtualbox(self, mock_run_command):
        setup_virtualbox()
        self.assertEqual(mock_run_command.call_count, 4)

    @patch('pyxconfig.run_command')
    def test_install_and_setup_nvidia_latest(self, mock_run_command):
        with patch('pyxconfig.get_driver_from_xdrivers', return_value='driver'):
            install_and_setup_nvidia('latest')
            self.assertTrue(mock_run_command.called)

    @patch('pyxconfig.run_command')
    def test_install_and_setup_nvidia_specific(self, mock_run_command):
        with patch('pyxconfig.get_driver_from_xdrivers', return_value='driver'):
            install_and_setup_nvidia('470')
            self.assertTrue(mock_run_command.called)

    @patch('pyxconfig.run_command')
    def test_setup_intel_drm(self, mock_run_command):
        setup_intel_drm()
        self.assertEqual(mock_run_command.call_count, 2)

    @patch('pyxconfig.run_command')
    def test_setup_amd_radeonkms_drm(self, mock_run_command):
        setup_amd_radeonkms_drm()
        self.assertEqual(mock_run_command.call_count, 2)

    @patch('pyxconfig.run_command')
    def test_setup_amdgpu_radeonkms_drm(self, mock_run_command):
        setup_amdgpu_radeonkms_drm()
        self.assertEqual(mock_run_command.call_count, 2)

    @patch('pyxconfig.run_command')
    def test_fail_safe(self, mock_run_command):
        fail_safe()
        self.assertTrue(mock_run_command.called)

    @patch('builtins.open', new_callable=mock_open, read_data='0x1234\n0x5678')
    def test_detect_radeon_device(self, mock_file):
        with patch('pyxconfig.run_command', return_value='0x1234'):
            self.assertTrue(detect_radeon_device())

    @patch('builtins.open', new_callable=mock_open, read_data='0x1234\n0x5678')
    def test_detect_radeon_device_not_found(self, mock_file):
        with patch('pyxconfig.run_command', return_value='0x9999'):
            self.assertFalse(detect_radeon_device())

    @patch('builtins.open', new_callable=mock_open, read_data='NVIDIA TITAN RTX\nNVIDIA TITAN V')
    def test_detect_nvidia_driver(self, mock_file):
        with patch('pyxconfig.run_command', return_value='NVIDIA TITAN RTX'):
            self.assertEqual(detect_nvidia_driver(), 'latest')

    @patch('builtins.open', new_callable=mock_open, read_data='NVIDIA TITAN RTX\nNVIDIA TITAN V')
    def test_detect_nvidia_driver_not_found(self, mock_file):
        with patch('pyxconfig.run_command', return_value='Some other GPU'):
            self.assertIsNone(detect_nvidia_driver())

    @patch('builtins.open', new_callable=mock_open, read_data='{"nvidia_device_files": {"latest": "config/nvidia_latest.txt"}}')
    def test_load_config(self, mock_file):
        config = load_config()
        self.assertIn('nvidia_device_files', config)

if __name__ == '__main__':
    unittest.main()

