FROM python:3.11.1

RUN mkdir /app
WORKDIR /app
#ADD .env /app
ADD requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt 
ADD . /app
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
EXPOSE 4000
CMD ["python","-u", "main.py"]