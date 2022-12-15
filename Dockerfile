FROM ubuntu:latest

RUN apt update
RUN apt install -y git
RUN apt install -y cmake
RUN apt install -y gfortran

RUN git clone https://gitlab.tudelft.nl/citg/wavemodels/swash.git
WORKDIR swash
RUN mkdir build
WORKDIR build
RUN cmake .. 
RUN cmake

