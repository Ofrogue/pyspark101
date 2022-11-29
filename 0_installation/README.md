You can find the installation guides for 
* [Windows](#installation-on-windows)
* [Mac](#installation-on-mac)  
* [Linux](#installation-on-linux)

We need to get installed:
* Java
* Miniconda (handy package management system for Python)
* PySpark (Python package to interact with Spark)
* Visual Studio Code (or any other IDE)

That should be enough to study Spark with Python.  
For Windows users we propose to use WSL for a smoother development process (see details in [Windows installation guide](#installation-on-windows)).

# Installation on Windows
## Requirements
Windows 10 / 11 Pro / Education
<!-- (Education can be activated by Taltech; login into Taltech Outlook and follow https://tallinn.onthehub.com/) -->


## Linux Subsystem
We will use Linux as our main tool for a better experience.
Microsoft is even pushing us to do so.

Modern Windows on a modern PC is capable of incorporating Linux as a component.
That is called WSL (Windows Subsystem Linux).
WSL is much faster than emulation of Linux with Virtual Box because utilises hardware feature of a modern CPU -- virtualization.
CPU understands when it runs a Guest's OS code and guards a Host OS from being compromized.
Say, the Guest OS is not able to escape from the sandbox and also runs with almost a native speed.



In cmd started as administrator:
```cmd
wsl --install -d ubuntu
```
Create user as promted, keep the password.  
Close cmd.

Now you can start Ubuntu as an application.
Run it from the Start menu.
It is a command line interface, but it is already Ubuntu -- a Linux distribution.

## Java
>In Ubuntu:
```sh
apt update
sudo apt install openjdk-8-jdk
```

## Conda
Conda is a handy package manager for python.  

Copy link for Miniconda3 Linux 64-bit at https://docs.conda.io/en/latest/miniconda.html#linux-installers

>In Ubuntu:
```sh
wget {link to Miniconda3 Linux 64-bit}
```
It should look like
```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
```

Run the downloaded file.
Something like  
>In Ubuntu:
```sh
sh Miniconda3-py39_4.12.0-Linux-x86_64.sh
```
and follow the installation process.  
Confirm initrc during installation.  
Restart Ubuntu terminal (close and open again application)

Then we create a separate python environment called ```spark-env``` and install minimal packages for it.
>In Ubuntu:
```sh
conda create -n spark-env 
conda activate spark-env 
conda install pip
pip install pyspark==3.2.1
```

## Visual Studio Code
We will use VScode as our main development tool.
Again, as Microsoft encourages us to do.
> In Windows

Install Visual Studio Code.  
Confirm addition to Path if asked during installation.

In VScode  install: 
* Remote Development extension  
* Python extension  

Open remote development tab on the left and choose connection to WSL Ubuntu.  
After connection is established a new VScode window will appear.  
In that window:
* Start an embedded console (Crl+j or drag from the bottom)
* Create a folder by typing 
     ```sh 
     mkdir parct0
     ```
* Go to File-> Open Folder
and choose the created folder. 
That should look like ```/home/{your username}/parct0```
* Go to View->Command Palette, search for ```python interpreter```,
choose a path to the conda environment
```/home/{user}/miniconda3/envs/spark-env/bin/python```

>In VScode console:
```sh
conda activate spark-env
```
## Installation test
>In VScode console
```sh
pyspark
```
That will satrt an interactive session.
If you can type ```spark``` and get no errors. most probably everything is set up correctly.

# Installation on Mac

Check Java version in terminal
```sh
java --version 
```
It should be something like:
```
java version "1.8.0_172"
Java(TM) SE Runtime Environment (build 1.8.0_172-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.172-b11, mixed mode)
```

Install miniconda  
Go to https://docs.conda.io/en/latest/miniconda.html  
And download the correct sh script.  
In terminal find the directory with the downloaded script and run something like
```sh
sh Miniconda3-latest-MacOSX-x86_64.sh
```
Confirm initrc during installation.

Run:
```sh
conda create -n spark-env 
conda activate spark-env 
conda install pip
pip install pyspark==3.2.1
```

Install IDE you like.
We propose Visual Studio Code with Python extension.
Create and open a folder in VScode.  
In VScode go to View->Command Palette, search for python interpreter, choose a path to the conda environment /home/{user}/miniconda3/envs/spark-env/bin/python

To test installation
Open embedded terminal in VScode (Cmd+j or drag from the bottom) and run 
```sh
conda activate spark-env
pyspark
```

# Installation on Linux
Install Java 8  
Install miniconda  
Create ```spark-env``` environment:
```sh
conda create -n spark-env 
conda activate spark-env 
conda install pip
pip install pyspark==3.2.1
```
Install IDE you like.
We propose Visual Studio Code with Python extension.

To test installation
```sh
conda activate spark-env
pyspark
```