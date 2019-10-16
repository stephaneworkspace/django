Building and Testing the Container
Now that you have the essentials in place, you can build your Docker image locally as follows:

docker build -t my-app .
This will go through all the commands in your Dockerfile, and if successful, store an image with your local Docker server that you could then run:

docker run -e DATABASE_URL='' -t my-app
This command is merely a smoke test to make sure uWSGI runs, and won't connect to a database or any other external services.

https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/