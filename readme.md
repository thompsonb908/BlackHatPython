1. Install Kali Linux and Windows 7 VMs
    1. Get Kali from https://www.kali.org/docs/installation/.
    2. Windows images from ...
2. Update Kali
    1. `sudo apt update`
    2. `sudo apt upgrade`
    3. `sudo apt dist-upgrade`
    4. `sudo apt autoremove`
    5. Install the `venv` package for Kali `sudo apt-get install python3-venv`
    6. Create a virtual environment: `python3 -m venv venv3`
    7. Activate the virtual environment with `source venv3/bin/activate`
3. Install python on Windows 7
    1. https://www.python.org/downloads/windows/
    2. Version 3.8.8 is the latest version for Windows 7
4. Install required packages
    1. `pip install -r requirements.txt`
