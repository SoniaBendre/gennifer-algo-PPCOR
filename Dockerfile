# Pull the base beeline dockerhub image
FROM python:3.8

ENV R_BASE_VERSION=3.5.3

RUN apt-get update && apt-get install r-base=${R_BASE_VERSION}-* r-base-dev=${R_BASE_VERSION}-* r-recommended=${R_BASE_VERSION}-* 

RUN R -e "install.packages('https://cran.r-project.org/src/contrib/ppcor_1.1.gz', type = 'source')"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# RUN apt-get update && apt-get install -y python3-pip

# Install the required packages
# RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask app
CMD ["flask", "run", "--host", "0.0.0.0"]
