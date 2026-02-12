FROM node:20-alpine

WORKDIR /app
COPY . /app
WORKDIR /app/frontend

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]
