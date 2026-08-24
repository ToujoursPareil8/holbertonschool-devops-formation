# Docker Volume Persistence with postgreSQL

## 1. Creation of a **named volume**

First, we create a named volume called pgdata. Fully managed by Docker (typically within WSL2 on Windows), they are safer and better optimized for database workloads than standard bind mounts.

```bash
docker volume create pgdata
```
**output and observation :** Docker simply outputs the name of te volume

```bash
$ docker volume create pgdata
pgdata
```

## 2. Run the intial PostgreSQL container

next, we start a PostgreSQM container in `-d` detached mode, we pass a mandatory environment variable(`POSTGRES_PASSWORD`) for initializaton. then we mount our named volume to /var/lib/postgresql (this is the default dir where pstgre image stores its db files). Adding `--pull=always`forces docker to contact the registry every time before starting the container allowing to always get the latest version of an image.
```bash
docker run -d --name my-postgres --pull=always -e POSTGRES_PASSWORD=mysecret -v pgdata:/var/lib/postgresql/ postgres
```

**Observation :** Docker pull the latest `postrges` image, creates the container and outputs the container ID. Db is starting in the background.

## 3. Write to the DB

**Test :** create some data to test persistence.

```bash
docker exec -it my-postgres psql -U postgres -c "CREATE TABLE holberton (id SERIAL PRIMARY KEY, note VARCHAR(255)); INSERT INTO holberton (note) VALUES ('data to survive destruction/deletion');"
```
the `docker exec` cmd is to run an interactive command inside the running container. calling psql to create a table and insert record.

**output and observation :** The terminal outputs `CREATE TABLE` followed by `INSERT 0 1` confirming that our table is initialized.

```Bash
$ docker exec -it my-postgres psql -U postgres -c "CREATE TABLE holberton (id SERIAL PRIMARY KEY, note VARCHAR(255)); INSERT INTO holberton (note) VALUES ('data to survive destruction/deletion');"
CREATE TABLE
INSERT 0 1
```
## 4. Verification

```bash
docker exec -it my-postgres psql -U postgres -c "SELECT * FROM holberton;"
```

output and observation : The terminal displays our table containing the inserted string.

```
id |                      note                      
----+------------------------------------------------
  1 | This data must survive the container destruction!
(1 row)
```

## 5. Remove container

```bash
docker stop my-postgres
docker rm my-postgres
```
**observation :** the container is stopped and then permanently deleted from the system.

## 6. Container recreation

We make a new container with a new name (`my_postgres-v2`), and we reattach the same named volume (`pgdata`) to the postgreSQL data path.
```bash
docker run -d --name my-postgres-v2 -e POSTGRES_PASSWORD=mysecret -v pgdata:/var/lib/postgresql/ postgres
```
**observation:** a new container is created and started.

## 7. Proof the data survived

finally, we query the new container to see our oiriginal data.
```bash
docker exec -it my-postgres-v2 psql -U postgres -c "SELECT * FROM holberton;"
```

**out and observation:** the output is identical to the first query.

```bash
$ docker exec -it my-postgres-v2 psql -U postgres -c "SELECT * FROM holberton;"
 id |                 note                 
----+--------------------------------------
  1 | data to survive destruction/deletion
(1 row)

```