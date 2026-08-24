FROM node:20-alpine

WORKDIR /usr/src/app

RUN addgroup app && adduser -S -G app app && chown -R app:app /usr/src/app
USER app

COPY --chown=app:app package*.json ./
RUN npm install
COPY --chown=app:app . .

HEALTHCHECK CMD wget --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
