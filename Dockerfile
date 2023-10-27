FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update 
RUN pip install --upgrade pip
WORKDIR /home/app
COPY . /home/app
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["sh","entrypoint.sh" ]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "core.wsgi"]