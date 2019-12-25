FROM continuumio/miniconda3

# docker build -t vanessa/juliart .

WORKDIR /code
COPY . /code
RUN python setup.py install
ENTRYPOINT ["juliart"]
