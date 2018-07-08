# PRKL Solution Documentation

## Dev environment
The dev environment is built on VirtualBox orchestrated by Vagrant

## AWS Architecture
![alt text](https://github.com/squeaky-godzilla/prkl/raw/master/docs/PRKL-Infra_AWS.jpg)
Since the primary dev environment was VM based, also the AWS architecture is designed using more traditional approach with EC2 instances.

### Architecture specifics
- since the API is fairly lightweight, it can be very easily deployed as a container or serverless Lambda function
- Lambda function would eliminate the need of ELB group
- deploying as a container would require building orchestrated solution on Kubernetes or Mesosphere or Docker Swarm, ideally utilizing managed solution by AWS
- solution management is handled via a bastion host placed in the public subnet

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
