To set up this project, first clone the repository and change directory to it.

Then, view the .env.example and create your own .env file that mimics the environment variables in the file and place it in the same directory as the .env.example. 

Once your .env file is set up, you just have to run `docker compose up --build` which should set up the docker container and image with installed dependencies.

Running `docker compose -f docker-compose-test.yaml up --build` will give dummy data for listings to view.

After the container is done being created, go to localhost:3000 to view the site.
