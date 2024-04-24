FROM node:18-alpine

WORKDIR /rentafriend-frontend

COPY public/ /rentafriend-frontend/public
COPY src/ /rentafriend-frontend/src
COPY package.json /rentafriend-frontend/

RUN npm install

CMD ["npm", "start"]