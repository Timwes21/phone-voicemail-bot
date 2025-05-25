FROM node:22.16-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

USER node

COPY . . 

EXPOSE 3000

CMD node server.js