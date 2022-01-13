ARG APP_IMAGE=python:3.9.7-alpine

FROM $APP_IMAGE AS base

FROM base AS builder
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt /requirements.txt
RUN pip install virtualenv && virtualenv /venv
RUN pip install wheel && pip install -r /requirements.txt

FROM base AS development
ENV PATH="/venv/bin:$PATH"
COPY --from=builder /venv /venv
WORKDIR /project
ADD . /project
ENV FLASK_APP app/app.py
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]

# TODO: Write a production image stage using uWSGI
