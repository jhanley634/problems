# Copyright 2024 John Hanley. MIT licensed.

# build with:
#     docker build -t pandoc .
#
# to get a bash prompt:
#     docker run -it pandoc

# Noble, LTS
FROM ubuntu:24.04

# minimal deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        curl \
        gnupg \
        lsb-release \
        iputils-ping \
        traceroute \
        telnet \
        wget \
    && true

# web + pandoc + LaTeX
RUN apt-get install -y \
        nginx \
        pandoc \
        texlive \
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-fonts-extra \
    && apt-get clean

WORKDIR /opt

ENTRYPOINT ["bash"]
