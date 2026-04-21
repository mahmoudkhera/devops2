FROM node:20-alpine as builder
WORKDIR /app

COPY package*.json ./
RUN npm install 

COPY . .

FROM gcr.io/distroless/nodejs20-debian12

WORKDIR /app

COPY --from=builder /app /app
CMD ["index.js"]