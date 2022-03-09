FROM python:3.8.6-buster
COPY requirements.txt /requirements.txt
COPY api /api
COPY opti_recruit /opti_recruit
COPY similarity_matrix.pickle /similarity_matrix.pickle
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
