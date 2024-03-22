#!/bin bash

# NOTE: move password to env variable

# Create docker container optibotx-postgres with user optibotx and database optibotx
docker run --name tracker-postgres -e POSTGRES_USER=tracker-wystakow -e POSTGRES_PASSWORD=12345678 -d -p 54350:5432 postgres
  