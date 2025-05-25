FROM node:22.16-slim

WORKDIR /app

COPY package.json ./

RUN npm cli --omit=dev

USER node

COPY . . 

EXPOSE 3000

CMD node server.js