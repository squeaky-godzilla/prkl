FROM python:2.7
WORKDIR /app
COPY app.py /app
COPY snippets /app
RUN pip install pymongo flask
ENTRYPOINT ["python"]
CMD ["app.py","10.5.0.6:27017"]
