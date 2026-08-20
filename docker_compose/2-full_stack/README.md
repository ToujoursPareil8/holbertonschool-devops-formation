# 2-full_stack

This configuration extends the stack by introducing a single entry point and a caching layer, while securing the internal network.

## Architecture & Traffic Flow
* **Reverse Proxy (Nginx)**: The only service exposing a port (8080). It routes `/api` traffic to the backend and all other traffic to the frontend.
* **Internal Isolation**: The `web` and `api` services no longer expose ports externally. They communicate securely within Docker's internal DNS.
* **Data Layer**: Includes a persistent Database (`db`) and an ephemeral Cache (`cache`), both running Redis with dedicated healthchecks.

## Usage

Bring the entire full-stack architecture up with one command:
```bash
docker compose up
```

there was too much logs to show here. ce n'était pas précisé s'il fallait le faire pour cette tache mais le compte README à quand-même été fait, au cas-où.