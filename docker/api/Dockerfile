FROM python:3.10

# Set the working directory
WORKDIR /home

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /home/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential

# Install Pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install application dependencies
RUN pipenv install --deploy --system

# Copy the application code to the working directory
COPY . /home

# Expose the application port
EXPOSE 8000
ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

#RUN pipenv shell
ENV ENV dev
RUN chmod +x /home/docker/api/startup.sh
ENTRYPOINT /home/docker/api/startup.sh
