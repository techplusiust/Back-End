# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install dependencies
RUN python3 manage.py import_professors professors/management/commands/golestan_courses_4022.xlsx


# Expose the port the app runs on
EXPOSE 8000


# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
