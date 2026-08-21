# 4 — Architecture

Documentation of the stack built in `docker_compose/2-full_stack/compose.yaml`.

## Diagram

```
                                   Host machine
                                   ────────────
                              published port 8080
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Docker network: default                       │
│                                                                      │
│   ┌───────────────┐                                                  │
│   │ reverse_proxy │  nginx:alpine                                    │
│   │  (port 8080)  │  reads nginx.conf (bind mount, read-only)        │
│   └──────┬────────┘                                                  │
│          │  location "/"   → proxy_pass http://web:80                │
│          │  location "/api"→ proxy_pass http://api:500 (see notes)   │
│          │                                                           │
│   ┌──────▼───────┐                               ┌──────────────────┐│
│   │     web      │  nginx:alpine                 │      api         ││
│   │   (no port)  │  serves ./web (bind mount)    │  build ./api     ││
│   │              │                               │ Flask + gunicorn-││
│   └──────────────┘                               │ less dev server  ││
│                                                  │                  ││
│                                                  │     (no port)    ││
│                                                  └────────┬─────────┘│
│                                                           │          │
│                                     redis.Redis(host="db")│          │
│                                                           ▼          │
│                                                    ┌───────────────┐ │
│                                                    │      db       │ │
│                                                    │  redis:alpine │ │
│                                                    │  (hit counter)│ │
│                                                    └───────────────┘ │
│                                                                      │
│                                                    ┌───────────────┐ │
│                                                    │     cache     │ │
│                                                    │  redis:alpine │ │
│                                                    │  (declared as │ │
│                                                    │  a dependency,│ │
│                                                    │  unused by    │ │
│                                                    │  app.py)      │ │
│                                                    └───────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

## Services and their role

| Service | Image / build | Published port | Role |
|---|---|---|---|
| `reverse_proxy` | `nginx:alpine` | `8080:80` (only service exposed to the host) | Single entry point. Routes `/` to `web` and `/api` to `api`, based on `nginx.conf`. |
| `web` | `nginx:alpine` | none | Serves the static frontend (`index.html`) from a bind-mounted `./web` folder. |
| `api` | built from `./api/` (Python/Flask) | none | Backend logic. On `GET /api`, increments a hit counter in `db` and returns it as JSON. |
| `db` | `redis:alpine` | none | Application data store — holds the `hits` counter used by `api`. Has a healthcheck (`redis-cli ping`) that `api` waits on before starting. |
| `cache` | `redis:alpine` | none | Declared alongside `db` with an identical healthcheck. `api` waits for it to be healthy too, but the current `app.py` never actually connects to it — it's provisioned but unused. |

## Networks

No custom network is declared in `compose.yaml`, so Compose creates a single implicit **default bridge network** for the project. All five services join it automatically and resolve each other by **service name** through Docker's embedded DNS (`web`, `api`, `db`, `cache`). This is what lets `reverse_proxy` reach `http://web:80`, and `api` reach `redis.Redis(host="db")`, without any hardcoded IPs.

Only `reverse_proxy` publishes a port to the host (`8080:80`); every other service is reachable exclusively from inside that network, which keeps `web`, `api`, `db`, and `cache` unreachable from outside the Docker host.

## Volumes

No named/managed volumes are defined. There are only two **bind mounts**:

- `./reverse_proxy/nginx.conf:/etc/nginx/nginx.conf:ro` — injects the routing config into `reverse_proxy`, read-only.
- `./web:/usr/share/nginx/html` — injects the static site into `web`.

`db` and `cache` have **no volume at all**. This means Redis's data directory lives only in the container's writable layer: the hit counter is **not persisted** — `docker compose down` (or any container removal) resets it to zero. This contradicts the stack's own README, which describes `db` as a "persistent Database" — as configured today it is just as ephemeral as `cache`.

## End-to-end request path

1. A client sends `GET http://localhost:8080/api`.
2. The host forwards it to the only published port, landing on `reverse_proxy` (nginx).
3. `reverse_proxy` matches the `location /api` block and forwards the request over the internal network to `api`.
   - **Known bug**: the config proxies to `http://api:500`, but the Flask app listens on port `5000` (see `app.py`: `app.run(host="0.0.0.0", port=5000)`). As written, this `location` cannot actually reach the API container — it should be `proxy_pass http://api:5000;`.
4. Assuming the port is corrected, `api` (Flask) handles the request: it calls `cache.incr('hits')` on a Redis client configured with `host='db'`, which resolves via Docker DNS to the `db` container.
5. `db` increments and returns the counter; `api` wraps it in a JSON response (`{"message": ..., "hits": ...}`).
6. The response travels back through `reverse_proxy`, which relays it to the client on port 8080.

For a static page request (`GET http://localhost:8080/`), the path is shorter: `reverse_proxy` matches `location /` and proxies straight to `http://web:80`, which serves `index.html` from its bind-mounted volume — no `api` or `db` involved.