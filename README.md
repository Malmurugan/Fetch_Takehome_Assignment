# Fetch_Takehome_Assignment

## Instructions

1. Open the command line at the project folder.
2. Run the docker file using the below command:

```
docker build -t <your_dockername> .
```
3. To run the docker use the below command:

```
docker run -d -p 3000:3000 <your_dockername>
```
Note: This application runs in port: 3000.

4. The flask application is hosted at http://localhost:3000

## Sample outputs (using postman):

Sample ouput for Endpoint: Process Receipts
- Path: /receipts/process
- Method: POST
- Payload: Receipt JSON
- Response: JSON containing an id for the receipt.

![post endpoint image](https://github.com/Malmurugan/Fetch_Takehome_Assignment/blob/main/screenshots/postman-post.png)

Sample output for Endpoint: Get Points
- Path: /receipts/{id}/points
- Method: GET
- Response: A JSON object containing the number of points awarded.

![get endpoint image](https://github.com/Malmurugan/Fetch_Takehome_Assignment/blob/main/screenshots/postman-get.png)


