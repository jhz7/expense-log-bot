# Use an official Node.js 22 image (ARM64 compatible for M1)
FROM node:22-bullseye

ARG NODE_ENV
ENV NODE_ENV ${NODE_ENV}
ENV TZ="America/Bogota"

RUN apt-get update \
  && apt-get install -y curl

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory inside the container
WORKDIR /usr/src/app

RUN chown -R node:node /usr/src/app

# Switch to the "node" user
USER node

# install and cache app dependencies
COPY --chown=node:node . .

# Install dependencies (use --only=production for smaller images if needed)
RUN npm install

# Command to run the app
CMD ["npm", "run", "start"]