# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

RUN apt get update && apt install -y iputils-ping && apt install vim

# Install required Python libraries
RUN pip3 install --upgrade scikit-learn numpy joblib requests --break-system-packages

# Copy all scripts and model
COPY ml_ids_impl.py .
COPY log_parser_1.py .
COPY anomaly_model.pkl .

# Run the IDS script by default
CMD ["python3", "ml_ids_impl.py"]
