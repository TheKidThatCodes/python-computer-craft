# docker build --tag neumond/python-computer-craft:<version> .
# docker run -it -p 8080:8080 neumond/python-computer-craft:<version>

FROM python:3.10-alpine
RUN apk add --update \
    gcc musl-dev \
    build-base

WORKDIR /wheels
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install wheel
RUN pip download cc-secure
RUN pip wheel -w . cc-secure
RUN ls -l

FROM python:3.10-alpine

WORKDIR /wheels
COPY --from=0 /wheels/*.whl ./wheels/
RUN pip install --no-index -f ./wheels cc-secure
WORKDIR /home
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 8080/tcp
ENTRYPOINT [ "python", "-m", "cc-secure.server" ]
