FROM python:3.10.2

RUN mkdir -p /usr/src/bot/

WORKDIR /usr/src/bot/

COPY . /usr/src/bot/

ARG KEY_TG=production
ENV KEY_TG="${KEY_TG}"

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]