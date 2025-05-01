# 1. Use official Python image as base
FROM python:3.10

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy all project files into the container
COPY . .

# 4. Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose port 5000 (Flask default)
EXPOSE 5000

# 6. Run your app when the container starts
CMD ["python", "run.py"]
