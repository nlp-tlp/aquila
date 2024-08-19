# Build the react app
FROM node:16.0.0-alpine as builder

WORKDIR /app

RUN rm -rf /app/node_nodules

COPY package*.json ./

RUN npm install

COPY bin ./bin/
COPY data_warehousing ./data_warehousing/
COPY helpers ./helpers/
COPY nlp ./nlp/
COPY public ./public/
COPY routes ./routes/
COPY views ./views/
COPY app.js ./
