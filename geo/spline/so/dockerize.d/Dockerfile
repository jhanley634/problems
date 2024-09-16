# Copyright 2024 John Hanley. MIT licensed.

# build with:
#     docker build -t pandoc .
#
# to get a bash prompt:
#     docker run -v /tmp/k:/tmp/k -it pandoc

# Noble, LTS
FROM ubuntu:24.04

# minimal deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        curl \
        iputils-ping \
        lsb-release \
        python3-pip \
        telnet \
        traceroute \
        wget \
    && true

# web + pandoc + LaTeX
RUN apt-get install -y \
        nginx \
        pandoc \
        texlive \
        texlive-fonts-recommended \
    && apt-get clean
#        texlive-latex-extra \
#        texlive-fonts-extra \

WORKDIR /opt

ENTRYPOINT ["bash"]
