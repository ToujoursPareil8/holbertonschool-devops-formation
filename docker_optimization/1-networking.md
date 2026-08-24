# Docker networking

## 1. Creation of custom bridge Network

First, create a new custom network named `holberton-net`. Docker will use the `bridge` driver for this network. containers on the default bridge can only communicate via **IP addresses, which are dynamic and can change every time a container restarts**. By creating a **custom bridge network**, Docker activates an embedded DNS server that allows containers to resolve and ping each other simply by using their container names.

```bash
docker network create holberton-net
```
**Observation:** Docker outputs the unique ID of the created network. Verify with with `docker network ls`

## 2. Run the first container (target)

Next, launch a Alpine Linux container, attach it to the new custom network using `--network` flag, name it `container-a` and give a cmd `sleep 3600` so it stays alive in the background for 3600 seconds instead of exiting immediately. Adding `--pull=always`forces docker to contact the registry every time before starting the container allowing to always get the latest version of an image.

```bash
docker run -d --name container-a --network holberton-net --pull=always alpine sleep 3600
```
**Output:**
```bash
latest: Pulling from library/alpine
56dceff11b33: Download complete 
f5124fb579e2: Download complete 
Digest: sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b
Status: Downloaded newer image for alpine:latest
ab71dc032667e735e80fbad55380566b363956d7d04acfbb870a58d2bbe6bf96
```
**Observation:** Docker pulls the latest `alpine` image, starts the container in detached mode and outputs the container ID

## 3. Run the second container (client)

Next, launch a second Alpine container on te **same network** container-b

```bash
docker run -d --name container-b --network holberton-net alpine sleep 3600
```
**Observation:** the second container starts in the background and is now sharing the `holberton-net` network with container-a

## 4. Test communication by name

Testing : Use `docker exec` to run a ping command from inside `container-b` targeting `container-a` strictly by its name (no IP address). we use `-c 3` to limit ping to 3 packets.

```bash
docker exec -it container-b ping -c 3 container-a
```
observation : the terminal output a successful ping response

```
PING container-a (172.22.0.2): 56 data bytes
64 bytes from 172.22.0.2: seq=0 ttl=64 time=0.345 ms
64 bytes from 172.22.0.2: seq=1 ttl=64 time=0.093 ms
64 bytes from 172.22.0.2: seq=2 ttl=64 time=0.092 ms

--- container-a ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.092/0.176/0.345 ms
```

observation : ping success. docker's internal DNS automatically joined the container-a to its internal IP address. This showd that using a custome bridge, containers can reliably discover and communicate with each other user their static container names.