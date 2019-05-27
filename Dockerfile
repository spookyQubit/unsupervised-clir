FROM conda/miniconda3
MAINTAINER Shantanu Agarwal shan@gmail.com

RUN conda install numpy
RUN conda install -c anaconda nltk
RUN python -m nltk.downloader all


WORKDIR /usr/src/app

COPY . .



