# One image with the whole workspace: the Go API also serves the built React app.
# Build from this folder:  docker build -t fitkit-workspace .

FROM node:22-alpine AS web
WORKDIR /web
COPY web/package.json web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY web/ ./
RUN npm run build

FROM golang:1.24-alpine AS api
WORKDIR /src
COPY api/go.mod api/go.sum ./
RUN go mod download
COPY api/ ./
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/api ./cmd/api

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=api /out/api /api
COPY --from=web /web/dist /web
ENV WEB_DIR=/web
EXPOSE 8080
ENTRYPOINT ["/api"]
CMD ["serve"]
