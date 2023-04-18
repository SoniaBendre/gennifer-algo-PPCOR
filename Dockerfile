# Pull the base beeline dockerhub image
FROM grnbeeline/ppcor:base

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents (including ppcor.r) into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask app
CMD ["flask", "run", "--host", "0.0.0.0"]
