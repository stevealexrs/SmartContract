FROM mcr.microsoft.com/devcontainers/base:debian

# install npm
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install npm

# install n node version management
RUN npm install -g n
RUN n 18.12.1

# install truffle (via npm)
RUN npm install -g node-gyp
RUN npm install -g truffle

# install foundry
USER vscode
RUN curl -L https://foundry.paradigm.xyz | bash
RUN ${HOME}/.foundry/bin/foundryup