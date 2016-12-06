

# Calico-Mesos Usage Guide with the Docker Containerizer
# http://docs.projectcalico.org/v2.0/getting-started/mesos/tutorials/docker



# Creating a Docker network and managing network policy
docker network create --driver calico --ipam-driver calico-ipam management-database
docker network create --driver calico --ipam-driver calico-ipam management-ui





# The Calico IPAM driver provides address assignment that is geared towards a Calico deployment where scaling is important, 
# and port-mapping for the containers is not required.

# The Calico IPAM driver assigns addresses with host aggregation - this is an efficient approach for Calico requiring fewer programmed routes.



# (Optional) Customizing the Calico IP Pool
#--------------------------------------------------------
# http://docs.projectcalico.org/v2.0/getting-started/docker/tutorials/basic

# The calico/node container starts, a default pool is created (192.168.0.0/16).
# To choose a different IP range or to enable IPIP, 
# by creating a Calico IP Pool using the calicoctl create command specifying the ipip and nat-outgoing options in the spec. 
# Here create a pool with CIDR 10.10.0.0/16.

cat << '__EOF__' | calicoctl create -f -
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.10.0.0/16
  spec:
    ipip:
      enabled: true
    nat-outgoing: true
__EOF__


# IPIP should be enabled when running in a cloud environment that doesn’t enable direct container to container 

# Create the network:
docker network create --driver calico --ipam-driver calico-ipam --subnet 10.10.0.0/16 management-database
docker network create --driver calico --ipam-driver calico-ipam --subnet 10.10.0.0/16 management-ui








curl -X POST -H "Content-Type:application/json" http://118.69.190.27:8080/v2/apps?force=true --data '
{
  "id": "dockercloud-hello-world",
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "dockercloud/hello-world",
      "network": "BRIDGE",
      "portMappings": [
        { "hostPort": 0, "containerPort": 80 }
      ],
      "forcePullImage":true
    }
  },
  "instances": 2,
  "cpus": 0.1,
  "mem": 128,
  "healthChecks": [{
      "protocol": "HTTP",
      "path": "/",
      "portIndex": 0,
      "timeoutSeconds": 10,
      "gracePeriodSeconds": 10,
      "intervalSeconds": 2,
      "maxConsecutiveFailures": 10
  }],
  "labels":{
    "HAPROXY_GROUP":"external",
    "HAPROXY_0_VHOST":"dockercloud-hello-world.${FQN}"
  }
}'

