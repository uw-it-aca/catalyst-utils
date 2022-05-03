# catalyst-utils

[![Build Status](https://github.com/uw-it-aca/catalyst-utils/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=main)](https://github.com/uw-it-aca/catalyst-utils/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/catalyst-utils/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/catalyst-utils?branch=main)

A set of utilities for supporting Catalyst at the University of Washington.

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (2.2, 3.2)
- Vue (3.x)
- Bootstrap (5.x)

## Development (using Docker)

Go to your repository

        $ cd catalyst-utils

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:8000/
