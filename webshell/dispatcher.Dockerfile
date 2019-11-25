# Provides a ttyd server and spawns shell containers on demand.
FROM ubuntu:18.04

# Install docker and ttyd
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
      docker-ce docker-ce-cli containerd.io wget
RUN mkdir /opt/ttyd && \
    chmod 0700 /opt/ttyd && \
    cd /opt/ttyd && \
    wget -O ttyd https://github.com/tsl0922/ttyd/releases/download/1.5.2/ttyd_linux.x86_64 && \
    chmod +x ttyd

# Run ttyd, spawning toolbox containers on connect via mounted Docker socket
# - ttyd sends SIGHUP to docker-init upon tab close, so that abandoned sessions are cleaned up (requires Docker Engine 19.03.5+)
# - the LINUX_IMMUTABLE capability is required for the append-only attributes set in pam_auth.py
# - as toolbox containers are spawned outside the control of an orchestrator, the home directory volume and
#   network (for pico API authentication) must be specified here
ENTRYPOINT ["/opt/ttyd/ttyd", "-p", "8080", "-O", "docker", "run", "-it", "-v=webshell-homes:/home", "--init", "--rm", "--cap-add=LINUX_IMMUTABLE", "--network=picoctf_webshell-auth", "picoctf/toolbox"]
EXPOSE 8080
