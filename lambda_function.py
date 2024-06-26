import json
import boto3
import csv
import io
import env
import datetime
from fastapi import Request, FastAPI, Body, HTTPException #maybe httpexception not necessary
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
lambda_handler = Mangum(app)
origins = ['http://localhost:5173', 'https://localhost:5173', 'http://sappientia-viverre.com', 'https://sappientia-viverre.com']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
s3Client = boto3.client('s3')
apiKey = os.environ['api_key']
bucket_name = os.environ['bucket_name']
file_name = os.environ['file_name']
exceptionCaseEmail = "a@a.com"

@app.get("/")
def root(request: Request):
    my_header = request.headers
    if my_header.get("X-API-KEY") != apiKey:
        raise HTTPException(status_code=404, detail="Method Not Allowed")
    
    s3_response = s3Client.get_object(Bucket=bucket_name, Key=file_name)
    print("s3_response:", s3_response)
    
    file_data = s3_response['Body'].read().decode('utf')
    print("file_data:", file_data)

    return {
        "statusCode": 200,
        "body": json.loads(file_data),
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            'Content-Type': 'text/html'
        }
    }

@app.post("/subscribe")
def push_csv(request: Request, email: str = Body(..., embed=True)):
    my_header = request.headers
    if my_header.get("X-API-KEY") != apiKey:
        raise HTTPException(status_code=404, detail="Method Not Allowed")
    
    s3_response = s3Client.get_object(Bucket=bucket_name, Key=file_name)
    existing_data = s3_response['Body'].read().decode('utf')
    
    csv_lines = existing_data.split('\n')
    fieldnames = csv_lines[0].split(',')
    
    # Update CSV with new data
    new_data = {
        "email": email,
        "date": datetime.datetime.now().isoformat()
    }

    # Append new data to the CSV lines
    new_csv_lines = csv_lines + [f"{new_data['email']},{new_data['date']}"]

    # Join the updated CSV lines back into a string
    updated_csv = '\n'.join(new_csv_lines)
    s3Client.put_object(Bucket=bucket_name, Key=file_name, Body=updated_csv)

    return {
        "statusCode": 200,
        "body": updated_csv,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            'Content-Type': 'text/html'
        }
    }

@app.post("/todo_post_blog")
def push_json(request: Request, email: str = Body(..., embed=True)):
    my_header = request.headers
    if my_header.get("X-API-KEY") != apiKey:
        raise HTTPException(status_code=404, detail="Method Not Allowed")
    
    if email == exceptionCaseEmail:
        raise HTTPException(status_code=405, detail="Method Not Allowed")
    
    s3_response = s3Client.get_object(Bucket=bucket_name, Key=file_name)
    existing_data = json.loads(s3_response['Body'].read().decode('utf'))
    
    new_data = {
        "email": email,
        "date": datetime.datetime.now().isoformat()
    }

    existing_data["data"].append(new_data)
    updated_json = bytes(json.dumps(existing_data).encode('UTF-8'))
    s3Client.put_object(Bucket=bucket_name, Key=file_name, Body=updated_json)

    return {
        "statusCode": 200,
        "body": json.loads(updated_json),
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            'Content-Type': 'text/html'
        }
    }
