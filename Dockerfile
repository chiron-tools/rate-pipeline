# Start from the base Lambda image for Python
FROM public.ecr.aws/lambda/python:3.8

# Install the external dependency (requests)
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /var/task/src/
COPY lambda_function.py .

# Set the CMD to invoke the Lambda function handler
CMD ["lambda_function.lambda_handler"]

