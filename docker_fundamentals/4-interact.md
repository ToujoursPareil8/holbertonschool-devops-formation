## Task 4 Interact

**Build image**
```bash
docker build -t first-python-app-configurable .
```
**Run the container with `-e`**
```bash
docker run -d -p 5000:5000 -e GREETING="Hello" first-python-app-configurable
$ curl http://localhost:5001
```
**Observed Output:** 
```bash
Hello
```
``-e` at run time: the value passed with `-e GREETING="Hello"` overrides the default set by ENV in the Dockerfile. same variable name, the flag passed at docker overides.

**Verify from inside with `exec`**
```bash
$ docker exec interact-demo printenv GREETING
```
**Observed Output:** 
```bash
Hello
```
This confirms the variable set at run time is visible inside the running container's environment.
**Inpect**
```bash
docker inspect interact-demo
```
this command allows to inspect directly int the container's stored environment.
**Clean up**
```bash
docker stop interact-demo
docker rm interact-demo
```
this stops and removes hte container.
