FROM golang:1.22 AS builder

WORKDIR /src
COPY . .
RUN go build -o /app/server .

FROM alpine:3.20
COPY --from=build /app/server /server
CMD ["/server"]
