# Node base iamge
FROM python:3.9-slim-buster

# Working Directory
WORKDIR /app

COPY ./requirements.txt /app
# Copy local directories to the current local directory of our docker image (/app)
COPY . .

#Install any needed dependencies 

RUN pip install --no-cache-dir -r requirements.txt

# Expose port to run the app
EXPOSE 5000

ENV FLASK_APP=run.py
#Run command
CMD ["flask", "run", "--host", "0.0.0.0"]