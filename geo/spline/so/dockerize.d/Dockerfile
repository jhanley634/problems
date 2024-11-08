# Copyright 2024 John Hanley. MIT licensed.

# build with:
#     (cd geo/spline/so/dockerize.d && docker buildx build -t pandoc .)
#
# to get a bash prompt:
#     docker run -v /tmp/k:/tmp/k -it pandoc

# Noble Numbat, 24.04 LTS
FROM ubuntu:noble

ENV DEBIAN_FRONTEND=noninteractive

# web + pandoc + LaTeX
#
#        texlive-latex-extra \
#        texlive-fonts-extra \
#
RUN apt-get update && \
    apt-get install -y \
        nginx \
        pandoc \
        texlive \
        texlive-fonts-recommended \
        bash \
        build-essential \
        curl \
        iputils-ping \
        lsb-release \
        python3-pip \
        python3-venv \
        pipenv \
        telnet \
        traceroute \
        wget \
    && (cd /usr/bin && ln -s python3 python) \
    && apt-get clean

WORKDIR /opt

ENTRYPOINT ["bash"]
