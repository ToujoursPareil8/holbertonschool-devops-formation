# 1-healthchecks

This configuration introduces a healthcheck for the database to prevent race conditions during startup.

## How the ordering is demonstrated

By running `docker compose up`, the terminal logs clearly show the two-phase startup sequence:
1. **Creation phase:** All containers (`db`, `api`, `web`) are `Created` almost instantly.
2. **Startup phase:** The `db` container starts first and enters a `Waiting` state while Docker executes the `redis-cli ping` command.
3. The `api` and `web` containers remain strictly in the `Created` state, not starting their internal processes.
4. Once the database healthcheck returns a successful exit code, the `db` status changes to `Healthy`.
5. Only after this confirmation does the `api` container transition to `Started`, followed by the `web` container.

there was too much logs to show here.