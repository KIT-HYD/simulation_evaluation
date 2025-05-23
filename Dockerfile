# Pull any base image that includes python3
FROM python:3.12

# add node
RUN apt-get update && apt-get install -y nodejs npm

# install the toolbox runner tools
RUN pip install \
    json2args \
    pandas \
    numpy \
    plotly \
    seaborn \
    matplotlib \
    plotly \
    scikit-learn \
    pathlib \
    statsmodels \
    jinja2

# if you do not need data-preloading as your tool does that on its own
# you can use this instread of the line above to use a json2args version
# with less dependencies
# RUN pip install json2args>=0.6.2

# Do anything you need to install tool dependencies here
RUN echo "Replace this line with a tool"

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

RUN cd /src/report && npm install

# copy the citation file - looks funny to make COPY not fail if the file is not there
COPY ./CITATION.cf[f] /src/CITATION.cff

WORKDIR /src
CMD ["python", "run.py"]
