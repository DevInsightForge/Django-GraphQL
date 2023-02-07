FROM nginx/unit:1.28.0-python3.10

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /code

# Install pipenv and compilation dependencies
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system -v


# Install application into container
COPY . /code
COPY unit.json /var/lib/unit/conf.json
RUN mkdir "log"
RUN mkdir "media"
