# Vagrant infrastructure for PRKL (Linux or MacOSX)

Good old fashioned VM based infrastructure for PRKL

## Prerequisites

You will need to install following things:
- VirtualBox: to emulate hypervisor
- Vagrant: to simplify the VM provisioning
- Ansible: to orchestrate provisioning and deployment

*frontend* folder holds frontend infrastructure information
*backend* folder holds backend infrastructure information

## Installation
- go to /infra/vagrant/ folder
- run the deployment playbook by `ansible-playbook deploy_prkl.yml -K`
- the playbook will need root privileges, hence the `-K`
