# picoCTF web shell

# Contains common tools and allows access via SSH or HTTPS webshell.

FROM ubuntu:18.04

# # Restore man pages and other tools for interactive use
# RUN yes | unminimize

# # Install shell tools
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
#     # archive tools
#     bzip2 \
#     gzip \
#     tar \
#     unzip \
#     zip \
#     # build tools
#     build-essential \
#     nasm \
#     perl \
#     python \
#     python3 \
#     ruby \
#     # common command line tools
#     dos2unix \
#     gawk \
#     grep \
#     jq \
#     sed \
#     silversearcher-ag \
#     # editors
#     bvi \
#     emacs-nox \
#     joe \
#     nano \
#     tweak \
#     vim-nox \
#     # forensics tools
#     foremost \
#     scalpel \
#     sleuthkit \
#     testdisk \
#     tshark \
#     # networking tools
#     curl \
#     netcat-openbsd \
#     socat \
#     traceroute \
    wget \
#     # terminal multiplexers
#     screen \
#     tmux \
#     # misc
#     expect \
    pandoc

# # Workaround for gdb 32-bit freeze error
# # (https://bugs.launchpad.net/ubuntu/+source/gdb/+bug/1845494)
# RUN apt-get purge gdb && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y \
#       gdb=8.1-0ubuntu3 && \
#     echo "gdb hold" | dpkg --set-selections

# # Install pam dependencies
# RUN apt-get update && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y \
#       libpam-python \
#       python-pip \
#       python-setuptools
# RUN pip install \
#       "pyOpenSSL==19.0.0" \
#       "cryptography==2.7" \
#       "requests==2.22.0"

# # Install system python2 tools
# # (relies on python-pip from previous step)
# # ipython 6.0 dropped support for python2
# RUN pip2 install \
#       "ipython<6.0" \
#       "ptpython" \
#       "pwntools"

# # Replace /bin/sh with wrapper script to preserve privilege
# # (https://github.com/picoCTF/picoCTF/issues/150)
# COPY sh_wrapper /tmp/sh_wrapper
# RUN chmod 0755 /tmp/sh_wrapper && \
#     mv /tmp/sh_wrapper /bin/sh

# # Set nano as the default editor
# RUN update-alternatives --set editor /bin/nano

# # Set up PAM authentication
# COPY ./pam_files/common-auth /tmp/common-auth
# RUN chmod 0644 /tmp/common-auth && \
#     mv /tmp/common-auth /etc/pam.d/common-auth
# RUN echo 'session [success=ok default=bad] pam_python.so pam_session.py' >> /etc/pam.d/sshd
# COPY ./pam_files/security /tmp/security
# RUN chmod 0644 /tmp/security/pam_auth.py && \
#     chmod 0644 /tmp/security/pam_session.py && \
#     chmod 0700 /tmp/security/sshkey_auth.py && \
#     mv /tmp/security /lib/security

# Install gotty
RUN mkdir /opt/gotty && \
    chmod 0700 /opt/gotty && \
    cd /opt/gotty && \
    wget https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz && \
    tar xzf gotty_linux_amd64.tar.gz

ENTRYPOINT ["/opt/gotty/gotty", "-w", "docker", "run", "-it", "--rm", "ubuntu"]
