#  Installing GHDL/cocotb/GTKWave

## Installation

The installation instructions have been tested with Ubuntu 22.04 and WSL
for Windows 10.

### Installing Windows Subsystem for Linux (WSL)

Windows only: WSL lets you run a Linux environment directly on windows,
giving you access to a Linux command-line tools and applications.
Install WSL or a different Linux system.

<https://techcommunity.microsoft.com/t5/windows-11/how-to-install-the-linux-windows-subsystem-in-windows-11/m-p/2701207>

The following steps assume you’re in a Linux environment.

### GHDL

To get GHDL v3 we will have to build from source. Note: do not install
GHDL using apt, the version that exists in the Ubuntu repository is the
older v1.

1: Install GNAT and make

As GHDL is written in Ada, we will need to install the Ada compiler
GNAT. We will also need make for compilation and to run our testbenches
in the future. In terminal use the commands:
```
sudo apt update
sudo apt install gnat
sudo apt install make
```
2: Download and extract GHDL source files

The version of GHDL we will be using can be found here:

- [<u>https://github.com/ghdl/ghdl/tree/5726f0eccf874b872ce0729aab42f587d915a3f5</u>](https://github.com/ghdl/ghdl/tree/5726f0eccf874b872ce0729aab42f587d915a3f5)

Download the project as a zip file. In terminal use the command:
```
wget https://github.com/ghdl/ghdl/archive/5726f0eccf874b872ce0729aab42f587d915a3f5.zip
```
Extract the zip file using the command:
```
unzip 5726f0eccf874b872ce0729aab42f587d915a3f5.zip
```
3: Build GHDL from source

Navigate into the extracted folder using the command
```
cd ghdl-5726f0eccf874b872ce0729aab42f587d915a3f5
```
Finally, configure and build using the following commands:
```
./configure --prefix=/usr/local
make
sudo make install
```
Verify the installation and version (3.0.0) by using the command
```
ghdl version
```


### Cocotb 

The Cocotb verification framework is available in the Python package
installer pip.

Cocotb requires Python 3.6 or newer. Check your installed version by
using the command
```
python3 --version
```
Next, install pip using the command
```
sudo apt install python3-pip
```
If pip was already installed, you might have to update it
```
python3 -m pip install --upgrade pip
```
Finally install cocotb

```
python3 –m pip install cocotb
```
Verify the installation and version (1.7.2) by using the command
```
cocotb-config –v
```
Ubuntu might not find cocotb-config immediately as it only adds the
cocotb install folder ~/.local/bin to its PATH variable if the folder
already existed during startup. If this happens, try again after either
restarting Ubuntu or using the command
```
source ~/.profile
```
### GTKWave 

Install the wave viewer GTKWave by using the command
```
sudo apt install gtkwave
```

2.1.4 Additional Python packages

We will finally need the pytest and numpy packages. Install these using
the commands:
```
python3 –m pip install numpy
python3 –m pip install pytest
```


