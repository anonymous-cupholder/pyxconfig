import os
import subprocess
import sys
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Determine the path to the config file relative to the script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, '..', 'pyxconfig.json')

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

config = load_config()

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with error: {e}")
        return None

def is_root():
    return os.geteuid() == 0

def setup_virtualbox():
    logging.info("Setting up virtualbox settings.. Please wait..")
    run_command(['sysrc', 'vboxguest_enable=YES'])
    run_command(['service', 'vboxguest', 'start'])
    run_command(['sysrc', 'vboxservice_enable=YES'])
    run_command(['service', 'vboxservice', 'start'])

def install_and_setup_nvidia(driver_version):
    logging.info(f"Installing and setting up NVIDIA driver version {driver_version}.. Please wait..")
    if driver_version == "latest":
        driver = get_driver_from_xdrivers('nvidia-driver')
        if driver:
            run_command(['pkg', 'add', f"/xdrivers/{driver}"])
        run_command(['kldload', 'nvidia-modeset'])
        run_command(['sysrc', '-f', '/etc/rc.conf', 'kldload_nvidia=nvidia-modeset'])
    else:
        driver = get_driver_from_xdrivers(f'nvidia-driver-{driver_version}')
        if driver:
            run_command(['pkg', 'add', f"/xdrivers/{driver}"])
        run_command(['kldload', 'nvidia-modeset'])
        run_command(['sysrc', '-f', '/etc/rc.conf', 'kldload_nvidia=nvidia-modeset'])

def get_driver_from_xdrivers(driver_name):
    if os.path.exists('/xdrivers'):
        result = run_command(['grep', driver_name, '/xdrivers/drivers-list'])
        if result:
            return result.split()[1]
    return None

def setup_intel_drm():
    logging.info("Setting up Intel (DRM).. Please wait..")
    run_command(['kldload', 'i915kms'])
    run_command(['sysrc', '-f', '/etc/rc.conf', 'kldload_i915kms=i915kms'])

def setup_amd_radeonkms_drm():
    logging.info("Setting up AMD/Radeon (KMS DRM).. Please wait..")
    run_command(['kldload', 'radeonkms'])
    run_command(['sysrc', '-f', '/etc/rc.conf', 'kldload_radeonkms=radeonkms'])

def setup_amdgpu_radeonkms_drm():
    logging.info("Setting up AMD/ATI (amdgpu/radeon DRM).. Please wait..")
    run_command(['kldload', 'amdgpu'])
    run_command(['sysrc', '-f', '/etc/rc.conf', 'kldload_amdgpu=amdgpu'])

def fail_safe():
    logging.warning("No supported driver found. Falling back to VESA.")
    run_command(['cp', os.path.join(config['card_detect_directory'], 'XF86Config.vesa'), '/etc/X11/xorg.conf'])

def manual_setup():
    card_type = input("Enter the type of graphics card (intel, radeon, nvidia, vesa, scfb, virtualbox, shell, reboot, exit): ").strip().lower()
    handlers = {
        'intel': setup_intel_drm,
        'radeon': setup_amd_radeonkms_drm,
        'nvidia': lambda: install_and_setup_nvidia(detect_nvidia_driver()),
        'vesa': fail_safe,
        'scfb': lambda: run_command(['cp', os.path.join(config['card_detect_directory'], 'XF86Config.scfb'), '/etc/X11/xorg.conf']),
        'virtualbox': setup_virtualbox,
        'shell': lambda: os.system('/bin/sh'),
        'reboot': lambda: os.system('sudo reboot -q'),
        'exit': sys.exit
    }
    handler = handlers.get(card_type)
    if handler:
        handler()
    else:
        logging.error("Unknown option")

def auto_configure_x():
    global NVDRIVER
    if not NVDRIVER:
        if "VirtualBox" in run_command(['pciconf', '-lv']):
            setup_virtualbox()
        else:
            run_command(['pkg', 'delete', '-y', 'virtualbox-ose-additions'])
            if "vmware" in run_command(['pciconf', '-lv']):
                run_command(['cp', os.path.join(config['card_detect_directory'], 'XF86Config.vmware'), '/etc/X11/xorg.conf'])
            elif "Intel" in run_command(['pciconf', '-lv']):
                setup_intel_drm()
            elif detect_radeon_device():
                setup_amdgpu_radeonkms_drm()
            else:
                fail_safe()
    else:
        run_command(['pkg', 'delete', '-y', 'virtualbox-ose-additions'])
        install_and_setup_nvidia(NVDRIVER)

def load_nvidia_devices():
    nvidia_devices = {}
    for version, filename in config['nvidia_device_files'].items():
        with open(filename, 'r') as file:
            devices = file.read().splitlines()
            nvidia_devices[version] = devices
    return nvidia_devices

def detect_nvidia_driver():
    nvidia_devices = load_nvidia_devices()
    for version, devices in nvidia_devices.items():
        for device in devices:
            if device in run_command(['pciconf', '-lv']):
                return version
    return None

def detect_radeon_device():
    with open(config['radeon_device_file'], 'r') as file:
        radeon_devices = file.read().splitlines()
    for device in radeon_devices:
        if device in run_command(['pciconf', '-lv']):
            return True
    return False

def main():
    if not is_root():
        logging.error("You must be root to run pyxconfig")
        sys.exit(1)

    global NVDRIVER
    NVDRIVER = detect_nvidia_driver()
    TOSTART = sys.argv[1] if len(sys.argv) > 1 else None

    if TOSTART == 'setup':
        manual_setup()
    elif TOSTART == 'auto':
        auto_configure_x()
    else:
        manual_setup()

if __name__ == "__main__":
    main()

