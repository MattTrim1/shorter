FROM node AS base

WORKDIR /app/shorter
COPY package*.json ./
RUN npm install
ENV PATH /app/shorter/node_modules/.bin:$PATH

FROM base AS devel

EXPOSE 3000
CMD ["npm", "start"]

FROM base AS prod

COPY . .
RUN npm run build && npm install -g serve
CMD ["serve", "-s", "build"]