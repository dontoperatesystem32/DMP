# Use the official Node.js image as the base image (LTS version)
FROM node:20.14.0-alpine3.20

# Install tzdata for time zone configuration
RUN apk add --no-cache tzdata

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Specify the command to run the application
CMD ["node", "index.js"]
