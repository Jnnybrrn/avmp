# avmp - Automated Virtual Machine Provisioner

## Introduction
avmp is tool which can be used to easily define, configure and deploy Virtual Machines. It uses Vagrant under the hood, and aims to be useful for local testing and development.

Key features:
- Simple Configuration - Human readable and simple syntax
- Lightweight - requires just a single file to define your required environment
- Repeatable - able to be torn down and recreated in one command

## Installation
Installation of avmp is as simple to as cloning this repository into a desirable location.

During operation, avmp will save all of its files into the `WORK_DIR` defined by `avmp.conf` (defaults to `~/avmp`).

To run it however, you will need the following software installed.

#### Requirements
- **Vagrant** - 1.9.2+, available [here](https://www.vagrantup.com/downloads.html)
- **VirtualBox** - 5.1.16+, available [here](https://www.virtualbox.org/wiki/Downloads)
- **Python** - 2.7.x, available [here](https://www.python.org/download/releases/)
- **PyYAML (Python Package)** - 3.11+, available [here](http://pyyaml.org/wiki/PyYAML) or via pip `pip install pyyaml`
- **Jinja2 (Python Package)** - 2.9.5+, available [here](https://pypi.python.org/pypi/Jinja2) or via pip `pip install jinja2`

*It's recommended to get Vagrant and VirtualBox directly, package repositories typically provide a version far behind.*

## Getting Started
Once installed, it's recommended to check out the examples provided ([`webserver.yaml`](#examples) and [`devenvironment.yaml`](#examples)).

If you simply wish to get started working on your own configuration, create a `.yaml` file and begin to describe your required environment.

Once it's complete us the command;
```
./avmp.py <yourfile.yaml> up
```
to create the Virtual Machines described.

With your machines running, you can check `status`, `ssh` into, re-`provision` or `destroy` them using the respective command. For more information, try `./avmp.py -h` or `./avmp.py --help`.

## Examples
#### webserver.yaml
```yaml
avmpName: "webserver"

machines:
  - name: webserver
    box: debian/contrib-jessie64
    hostname: example-webserver
    scripts:
      - path: "scripts/webserver-setup.sh"
    synced_folders:
      - src: sync/apache
        dest: /var/www/
      - src: sync/apacheconfig
        dest: /etc/apache2
    network:
      type: private_network
      details:
        ip: 192.168.3.67
```

This example creates a Virtual Machine running Apache2, linking in a local folder `sync/apache` as the hosted directory and `sync/apacheconfig` as the Apache config directory.

#### DevEnvironment.yaml
```yaml
avmpName: "devenvironment"

machines:
  - name: devenvironment
    box: debian/contrib-jessie64
    hostname: example-devenvironment
    scripts:
      - inline: "sudo apt-get update; sudo apt-get install -y default-jdk"
    synced_folders:
      - src: sync/devEnv
        dest: /devEnv
    network:
      type: public_network # dhcp
```

This example creates a Virtual Machine with the Java SDK installed, it links in `sync/devEnv` which contains the simple `HelloWorld.java` class. It can be used as a environment to run/debug Java code by ssh'ing into the VM (`./avmp.py devenvironment.yaml ssh`).

## Contribute
If you want to report a bug or problem, simply leave a GitHub Issue, or fix it and submit a pull request!
