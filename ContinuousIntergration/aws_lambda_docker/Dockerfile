FROM python:3.10-slim-bullseye

RUN mkdir /opt/extensions
RUN mkdir /opt/disable-extensions-jwigqn8j
RUN chmod 755 /opt/extensions /opt/disable-extensions-jwigqn8j

RUN pip install awslambdaric
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY ./entry.sh "/entry.sh"
RUN chmod 755 /entry.sh

ARG APP_DIR="/home/app/"
WORKDIR ${APP_DIR}
COPY /app ${APP_DIR}
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["/entry.sh"]
CMD ["app.handler"]
