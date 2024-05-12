FROM node:18-alpine

WORKDIR /rentafriend-frontend

COPY package.json /rentafriend-frontend/
COPY public/ /rentafriend-frontend/public
COPY src/ /rentafriend-frontend/src

RUN npm install

CMD ["npm", "start"]