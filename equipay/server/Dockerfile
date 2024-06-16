FROM python:3.12
WORKDIR /server
COPY . /server
RUN ls -la /server
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./src/server.py
