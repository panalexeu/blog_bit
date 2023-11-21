FROM python:3.9
LABEL authors="Oleksii"

ENV FLASK_APP blog_bit.py
ENV FLASK_CONFIG production
ENV FLASK_DEBUG 0
ENV MAIL_PASSWORD 'bbuj bdmu ufwx ytjf'
ENV MAIL_USERNAME alexeu.debug@gmail.com

WORKDIR /blog_bit

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /blog_bit

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "blog_bit:app"]