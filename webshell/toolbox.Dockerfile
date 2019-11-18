# picoCTF webshell toolbox

# Shell image containing various hacking tools.

FROM ubuntu:18.04

# Restore man pages and other tools for interactive use
RUN yes | unminimize

# Install shell tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    # archive tools
    bzip2 \
    gzip \
    tar \
    unzip \
    zip \
    # build tools
    build-essential \
    nasm \
    perl \
    python \
    python3 \
    ruby \
    # common command line tools
    dos2unix \
    gawk \
    grep \
    jq \
    sed \
    silversearcher-ag \
    # editors
    bvi \
    emacs-nox \
    joe \
    nano \
    tweak \
    vim-nox \
    # forensics tools
    foremost \
    scalpel \
    sleuthkit \
    testdisk \
    tshark \
    # networking tools
    curl \
    netcat-openbsd \
    socat \
    traceroute \
    wget \
    # terminal multiplexers
    screen \
    tmux \
    # misc
    expect \
    pandoc

# Workaround for gdb 32-bit freeze error
# (https://bugs.launchpad.net/ubuntu/+source/gdb/+bug/1845494)
RUN apt-get purge gdb && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      gdb=8.1-0ubuntu3 && \
    echo "gdb hold" | dpkg --set-selections

# Install pam dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
      libpam-python \
      python-pip \
      python-setuptools
RUN pip install \
      "pyOpenSSL==19.0.0" \
      "cryptography==2.7" \
      "requests==2.22.0"

# Install system python2 tools
# (relies on python-pip from previous step)
# ipython 6.0 dropped support for python2
RUN pip2 install \
      "ipython<6.0" \
      "ptpython" \
      "pwntools"

# Set nano as the default editor
RUN update-alternatives --set editor /bin/nano
