FROM node:20-alpine

WORKDIR /usr/src/app

RUN addgroup app && adduser -S -G app app
USER app

COPY package*.json ./
RUN npm install
COPY . .

HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1

CMD ["node", "server.js"]
