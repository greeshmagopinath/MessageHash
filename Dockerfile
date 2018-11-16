FROM python:3-onbuild
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install -e .
CMD ["python", "MessageHash/app.py"]
