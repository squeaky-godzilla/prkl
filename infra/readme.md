# Infrastructure for PRKL

*frontend* folder holds frontend infrastructure information
*backend* folder holds backend infrastructure information

## Architecture & deployment

nginx proxy loadbalancer --- frontend API server (hosts FLASK) --- backend MongoDB cluster

- Built on Vagrant with VirtualBox virtualization
- Box: 'hashicorp/precise64'
- Using Ansible for config management

## Backend architecture

- datastore backend is MongoDB database
- (clustered for scaling)
