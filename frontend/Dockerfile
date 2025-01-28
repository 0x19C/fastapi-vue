# build stage
FROM node:20.18.1

RUN mkdir app
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

CMD ["npm", "run", "preview"]