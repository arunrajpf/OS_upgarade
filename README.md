# In-place Migration from RHEL 7 to RHEL 8

<br>

# Overview

This repository contains Ansible Playbooks for performing an in-place upgrade on a Virtual Machine, migrating from RHEL 7 to RHEL 8.

Please note a few things to note before you begin:

- :warning: Running these playbooks against your virtual machine may cause your application to break. Please make sure you have a backup of your virtual machine before running these playbooks, and that your application is properly load-balanced.

- :x: This upgrade is not recommended for virtual machines that are in a public cloud environment. It is recommended that you re-image your Oracle RAC Server with RHEL 8 instead.

- This upgrade will not support an in-place migration of Python v3.6. You must uninstall Python 3.6 before running the upgrade, clean up any Python 3.6 packages you may have installed, and reinstall it after the upgrade.


<br>

# Table of Contents

- [Prerequisites](#prerequisites)
- [Steps](#steps)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Create Inventory file with list of hosts](#create-inventory-file-with-list-of-hosts)
  - [Patch your host(s) using the tie-builder-playbooks repo](#patch-your-hosts-using-the-tie-builder-playbooks-repo)
  - [Upgrade your host(s) with Leapp Playbooks](#upgrade-your-hosts-with-leapp-playbooks)
  - [Post Upgrade Patching & Hardening your Host(s)](#post-upgrade-patching--hardening-your-hosts)

<br>

# Prerequisites

- Local virtual environment with [Ansible v2.14.6](https://pypi.org/project/ansible/) installed
- SSH access to [Github Enterprise Cloud](https://help.github.com/en/enterprise/2.21/user/github/authenticating-to-github/connecting-to-github-with-ssh)

<br>

# Steps

## Create a Virtual Environment

  ``` shell
  # Create a directory to store your virtual environment
  mkdir ~/venvs/ansible-2.14.6

  # Change to the directory you just created
  cd ~/venvs/ansible-2.14.6

  # Create a virtual environment named "ansible-2.14.6"
  python3 -m venv ansible-2.14.6

  # Activate the virtual environment
  source ansible-2.14.6/bin/activate
  
  # Install Ansible v2.14.6
  pip install ansible-core==2.14.6
  ```

<br>

## Create Inventory file with list of hosts

``` shell
# Create an inventory file with a list of hosts
vi /var/tmp/RHEl7to8.inv

# Insert your list of hosts in the file
100.88.63.14 # sample host IP
100.88.63.13 # sample host IP

# ESC :wq!
```

<br>  

## Patch your host(s) using the tie-builder-playbooks repo
Note:- Don't Update your hosts if it is oracle rac or oracle standalone server as oracle doesn't support latest and greatest patchset
- Patch your host(s) using the tie-builder-playbooks repo:

  ``` shell
  # Clone tie-builder-playbooks repo locally
  git clone git@github.comcast.com:APS-INFRA/tie-builder-playbooks.git

  # Change to root of project
  cd tie-builder-playbooks

  # Install tie-builder-playbooks Ansible Roles
  ansible-galaxy install -r roles/requirements.yml -p roles

  # Install tie-builder-playbooks Ansible Collections (this may not be necessary)
  ansible-galaxy collection install -r collections/requirements.yml -p collections

  # Get a fresh Autobahn token
  jump -uci

  # Run the patch.yml playbook to patch your host(s)
  ansible-playbook patch.yml --tags "ppstie_frozen_repo,update_packages" -e "ppstie_frozen_repo_patchset=current" -i /var/tmp/centos2rocky.inv -u autobahn -b
  ```

<br>

## Upgrade your Host(s) with Leapp Playbooks

- Upgrade your RHEL 7 host(s) to RHEL 8 using the Leapp playbooks
  ``` shell
  # Clone the rhel7-to-8 repo locally
  git@github.comcast.com:APS-INFRA/rhel7-to-8-migration.git

  # Change to root of project
  cd rhel7-to-8-migration

  # Run the Leapp pre upgrade playbook
  ansible-playbook leapp-prep-work.yml -i /var/tmp/RHEl7to8.inv -u autobahn -b

  # Run the Leapp upgrade playbook
  ansible-playbook leapp-upgrade.yml -i /var/tmp/RHEl7to8.inv -u autobahn -b

  # Run the Leapp post upgrade playbook
  ansible-playbook leapp-post.yml -i /var/tmp/RHEl7to8.inv -u autobahn -b
  ```

<br>

## Post Upgrade Patching & Hardening your Host(s)
Note:- Don't Update your hosts if it is oracle rac or oracle standalone server as oracle doesn't support latest and greatest patchset
- There are two ways to patch/harden your host(s):

  - Use the [Shield/Patcher](https://devhub.de.comcast.net/#/services/patcher) service.

    - > Note: If you need cada authentication, you can patch and harden through Shield/Patcher, then apply the cada roles using the standard.yml playbook in the tie-builder-playbooks repo. If you do not apply the cada roles, you will not be able to login to your host(s) using cada.
    
    <br>

  - Use the [tie-builder-playbooks](https://github.comcast.com/APS-INFRA/tie-builder-playbooks) patch, harden, and standard playbooks. This is the recommended method if you require cada authentication.
