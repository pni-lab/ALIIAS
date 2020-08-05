FROM python
#Alpine Linux OS

RUN pip install flask pycryptodome limesurveyrc2api

WORKDIR /usr/app/
COPY . /usr/app/
COPY ./dev_key /key
# todo do not copy key!!

#RUN pip install -r requirements.txt

ENV FLASK_APP=pseudoID
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0 --port=80
