FROM python:alpine

RUN addgroup -S webapp && adduser -S user -G webapp --uid 1000


RUN mkdir /home/user/cache
RUN chown user:webapp /home/user/cache

RUN mkdir /home/user/data
RUN chown user:webapp /home/user/data

RUN mkdir /home/user/images
RUN chown user:webapp /home/user/images

RUN apk add gcc musl-dev linux-headers python3-dev

USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH

RUN pip install --no-cache-dir --upgrade pip

COPY --chown=user:webapp requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user:webapp ./cache/* ./cache/
COPY --chown=user:webapp ./data/* ./data/ 
COPY --chown=user:webapp ./images/* ./images/

COPY --chown=user:webapp fantasy_teams.py fantasy_teams.py
COPY --chown=user:webapp webapp.py webapp.py

EXPOSE 8080
ENTRYPOINT ["solara", "run", "webapp.py", "--host=0.0.0.0", "--port", "8080", "--production"]


