FROM node AS base

WORKDIR /usr/src/app/shorter
COPY package*.json ./
RUN npm install

FROM base AS devel

EXPOSE 3000
CMD ["npm", "start"]

FROM base AS prod

COPY . .
RUN npm run build && npm install -g serve
CMD ["serve", "-s", "build"]