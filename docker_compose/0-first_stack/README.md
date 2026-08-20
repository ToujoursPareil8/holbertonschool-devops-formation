# 0-first_stack

This is a complete 3-tier architecture containing a Web Front (Nginx), an API (Python/Flask), and a Database (Redis), managed entirely by Docker Compose.

## Requirements
**Docker Desktop** 
Git bash

## How to run the stack

To bring the whole thing up at once, run:
```bash
docker compose up -d --build
```
--build flag ensures the custom API image is built. -d flag runs the container in the bg, keeping your terminal free.

## How to stop 

```bash
docker compose down