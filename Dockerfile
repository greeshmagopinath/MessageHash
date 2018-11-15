FROM python:3-onbuild
RUN pip install -r requirements.txt
RUN pip install -e .
CMD ["python", "MessageHash/app.py"]
