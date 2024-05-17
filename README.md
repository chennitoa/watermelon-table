# Rent a Lackey
By Austin Chen, Andrew Vu, Stanley Nguyen, Anshul Jha


## About

Rent a Lackey is a web application that connects everday people together to complete the small jobs that you can't complete. Rent a Lackey features the ability for users to post short job listings and contact nearby job posters to discuss accepting their jobs. 

## Setup

To set up this project, first clone the repository and change directory to it.

Then, create a `.env` file to the following specifications:

```
MYSQL_HOST=""
MYSQL_USER=""
MYSQL_PASSWORD=""
MYSQL_DATABASE=""
MYSQL_ROOT_PASSWORD=""
MYSQL_PORT=""
SECRET_KEY=""
GMAPS_APIKEY=""
MONGO_URI=""
```

Do not set `MYSQL_USER` to `root`. A seperate user must be created.

The `MYSQL_HOST` variable should be `host.docker.internal`.

The `MYSQL_PORT` variable should be `3305`.

`GMAPS_APIKEY` must be created as a Google Maps API key. You must have a Google Cloud account to use this.

`MONGO_URI` is the URI to a MongoDB instance. Create a cloud MongoDB instance if needed.

All values should be surrounded in double quotes.

The specifications are also viewable in `.env.example`.

Once your .env file is set up, you just have to run `docker compose up --build` which should set up the docker container and image with installed dependencies.

Running `docker compose -f docker-compose-test.yaml up --build` will give dummy data for listings to view.

After the container is done being created, go to localhost:3000 to view the site.
