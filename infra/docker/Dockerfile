FROM python:2.7
WORKDIR /app
COPY api_functions.py /app
RUN pip install pymongo flask
ENTRYPOINT ["python"]
CMD ["api_functions.py"]
