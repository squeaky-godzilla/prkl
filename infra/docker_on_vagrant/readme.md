# Docker on Vagrant box

## How does this work?

This will install Docker and Docker Compose on a VM.

## Prerequisites

Install Ansible 2.6, VirtualBox and Vagrant

## Installation

go to the /infra/docker_on_vagrant folder and run `vagrant up`
the box should be ready in about 10 minutes.

## Usage
Vagrant will forward the :5000 port to your host machine, so you will be able to reach the API on http://localhost:5000/songs/

you can also `vagrant ssh` to the box to look at the internals.
