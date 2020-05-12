FROM node:latest

RUN npm install -g @vue/cli

# Should mount some volume in code
WORKDIR /code

CMD ["/usr/local/bin/yarn", "build"]