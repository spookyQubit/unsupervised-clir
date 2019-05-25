FROM conda/miniconda3
MAINTAINER Shantanu Agarwal shan@gmail.com

RUN conda install numpy

WORKDIR /usr/src/app

COPY . .



