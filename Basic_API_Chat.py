# Purpose of program is to chat with a PDF document
# Import libraries
import requests
import json

# Replace with your API key
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Replace with the path to your PDF file
file_path = '/home/rnd-home/Documents/Fun Stuff/AskPDF/Stock_Market.pdf'

headers = {
    'x-api-key': api_key
}

file_data = open(file_path, 'rb')

# Let's upload the document and get a doc_id

response = requests.post('https://api.askyourpdf.com/v1/api/upload', headers=headers,
 files={'file': file_data})

if response.status_code == 201:
    print(response.json())
else:
    print('Error:', response.status_code)

# Let's extract just the doc_id for the document

doc_id = response.json().get('docId')
print("The document ID is",doc_id)

# Let's chat with the document
data = [
    {
        "sender": "User",
        "message": "Who wrote this document?"
    }
]

response = requests.post(f'https://api.askyourpdf.com/v1/chat/{doc_id}', 
headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print(response.json().get('answer', {}).get('message'))
else:
    print('Error:', response.status_code)

# Next question

data = [
    {
        "sender": "User",
        "message": "Summarize this document for me. What are the key points?"
    }
]

response = requests.post(f'https://api.askyourpdf.com/v1/chat/{doc_id}', 
headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print(response.json().get('answer', {}).get('message'))
else:
    print('Error:', response.status_code)
