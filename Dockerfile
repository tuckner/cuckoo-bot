FROM python:2.7
ARG slack_client=
ARG cuckoo_api=
ENV slack=$slack_client
ENV cuckoo=$cuckoo_api
RUN git clone https://github.com/tuckner/cuckoo-bot.git /src/
WORKDIR /src
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]
