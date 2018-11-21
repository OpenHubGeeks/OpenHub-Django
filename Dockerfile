 FROM python:3.5.2
 EXPOSE 8000
 EXPOSE 5920
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /openhub
 WORKDIR /openhub
 COPY requirements.txt /openhub/
 RUN pip install -r requirements.txt
 ADD . /openhub/
 COPY wait-for-it.sh /usr/local/bin/
 RUN chmod +x /usr/local/bin/wait-for-it.sh