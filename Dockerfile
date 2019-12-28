FROM continuumio/miniconda3

# docker build -t quay.io/vanessa/juliart .

WORKDIR /code
COPY . /code
RUN python setup.py install && \
    pip install .[animate]
ENTRYPOINT ["juliart"]
