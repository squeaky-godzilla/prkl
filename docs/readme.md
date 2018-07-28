# PRKL Solution Documentation

## Dev environment
The dev environment is built on VirtualBox orchestrated by Vagrant. Ansible is used as the main config management & deployment tool.

## AWS Architecture
![alt text](https://github.com/squeaky-godzilla/prkl/raw/master/docs/PRKL-Infra_AWS.jpg)
Since the primary dev environment was VM based, also the AWS architecture is designed using more traditional approach with EC2 instances.

### Architecture specifics
- since the API is fairly lightweight, it can be very easily deployed as a container or serverless Lambda function
- Lambda function would eliminate the need of ELB group
- deploying as a container would require building orchestrated solution on Kubernetes or Mesosphere or Docker Swarm, ideally utilizing managed solution by AWS
- solution management is handled via a bastion host placed in the public subnet

### Scaling for spike traffic
accommodating spike traffic can be done in following ways:

- building fewer instances large enough to accomodate spike (scale up)
- building many smaller instances (scale out)

Application frontend (FLASK) is not performance optimized for scale up approach,
however it's very well suited for scaling out onto smaller instances, be it small EC2 instances or containers.

The scale out can be automated by enabling autoscaling group and elastic loadbalancer in AWS, or by observing the traffic spike pattern and scheduling the scale out accordingly. The autoscaling group method is not very efficient for sudden workload spikes.

The selected backend (MongoDB) is also a scale out friendly infrastructure (although there are scale up deployments of the technology as well), however the scaling of it's components is more complex than the Flask frontend. In the case of MongoDB, I'd suggest careful analytics of the compute and storage capacity demand and adjust the growth strategy. Because the datastore and query processing function is decoupled, it gives options to achieve optimal performance even in large data volumes.

### Request processing:
- user request comes through the internet gateway
- DNS service Route 53 directs it to the Elastic Load Balancer
- ELB directs the request to the relevant EC2 instance
- EC2 instance initiates connection to MongoDB query router
- MongoDB query router reaches out to relevant shards to complete the query
- output is returned to the PRKL API on EC2 instance and passed to the user

### Monitoring and alerting
- There is an option to use relevant AWS services or build a solution deployed on ie. EC2 or EKS
- Absolute basics for tracking numeric metrics is a TSDB solution, either CloudWatch or EC2 based InfluxDB (or other TSDB) coupled with Grafana or New Relic visualization
- for log analysis I suggest using either Splunk or ELK stack (ElasticSearch, Logstash, Kibana), combined with Kinesis

### CICD pipeline
![alt text](https://github.com/squeaky-godzilla/prkl/raw/master/docs/PRKL_CICD.jpg)

Here is a simple suggestion how a multi environment deployment can be done with combination of Jenkins, Artifactory and Docker.
