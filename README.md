- API scheme is presented in petsauction-schema.yml
- Run `docker-compose up --build` in root folder to launch the docker containers. The backend should be available at http://localhost:8000/
- First of all one needs to create a user at /api/users/ and get token at /api/auth-token/ -- the application uses token authentication for all post, put, patch and delete actions
