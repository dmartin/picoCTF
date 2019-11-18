# Provides a goTTY server and spawns shell containers on demand.
FROM ubuntu:18.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
      apt-key add - && \
    add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget docker-ce docker-ce-cli containerd.io

RUN mkdir /opt/gotty && \
    chmod 0700 /opt/gotty && \
    cd /opt/gotty && \
    wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz && \
    tar xzf gotty_linux_amd64.tar.gz

ENTRYPOINT ["/opt/gotty/gotty", "-w", "docker", "run", "-it", "--rm", "picoctf/toolbox"]
