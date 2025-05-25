FROM node:22.16-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

USER node

COPY . . 

EXPOSE 8080

CMD node index.js