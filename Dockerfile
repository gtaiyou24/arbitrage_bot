FROM centos:7

MAINTAINER Taiyo Tamura gtaiyou24@gmail.com

ARG PYTHON_VERSION='3.6.4'
ARG PROJECT_NAME='arbitrage_bot'

# pyenvをインストール
RUN yum -y update
RUN yum -y install kernel-devel kernel-headers gcc-c++ patch libyaml-devel libffi-devel autoconf automake make \
                   libtool bison tk-devel zip wget tar gcc zlib zlib-devel bzip2 bzip2-devel readline readline-devel \
                   sqlite sqlite-devel openssl openssl-devel git gdbm-devel python-devel unzip 

ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH

RUN git clone https://github.com/yyuu/pyenv.git $HOME/.pyenv
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    eval "$(pyenv init -)"

# python3をインストール
RUN pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION}

# 作業フォルダの作成
RUN mkdir -p $HOME/${PROJECT_NAME}
WORKDIR $HOME/${PROJECT_NAME}
ADD . $HOME/${PROJECT_NAME}