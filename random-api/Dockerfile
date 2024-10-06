# Specify the base image
FROM node:20.10.0-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

RUN npm install typescript -g

# Install dependencies
RUN npm i --production

# Copy the application code
COPY . .


# Build dist
RUN npm run build

# Port
EXPOSE 3000

# Specify the command to run your application
CMD [ "npm", "run", "dev" ]