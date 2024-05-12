FROM node:18-alpine

WORKDIR /rentafriend-frontend

COPY package.json .

RUN npm install

COPY public/ ./public
COPY src/ ./src

CMD ["npm", "start"]