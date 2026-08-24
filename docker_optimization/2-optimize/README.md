# Docker Optimization Results

| Metric | Baseline (`node:20`) | Optimized (`node:20-alpine`) | Improvement |
| :--- | :--- | :--- | :--- |
| **Image Size (Content)** | 401 MB | 50.8 MB | **~87% reduction** |
| **Disk Usage** | 1.59 GB | 208 MB | **~87% reduction** |
| **Initial Build Time** | 27.1 s | 5.0 s | **~5x faster** |
| **Rebuild Time (Code Change)** | 4.8 s | 1.0 s | **~5x faster (Cached)** |

### Optimization Breakdown

1. **Lighter Base Image:** Switched from the default `node:20` to `node:20-alpine`, significantly reducing the OS footprint.
2. **Layer Caching:** Reordered instructions to copy dependency files and run `npm install` before copying the application code. This ensures instant rebuilds when only source code is modified.
3. **.dockerignore:** Added a comprehensive `.dockerignore` file blocking local `node_modules` from polluting the build context and image content.
4. **Security:** Added the `USER node` instruction to ensure the application runs as a non-root user, adhering to the principle of least privilege.