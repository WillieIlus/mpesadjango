import base64
import json

import requests
from django.http import HttpResponse
from yourapp.models import YourModel


def mpay_generate(request):
    consumer_key = 'lOIGknrirnapyrzdKp5VavouJ6ABy0RR'
    consumer_secret = 'bMV32BQqTemWtGHA'
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((consumer_key + ':' + consumer_secret).encode('utf-8')).decode(
            'utf-8')
    }
    response = requests.get(url, headers=headers)
    access_token = json.loads(response.text)['access_token']
    return access_token



def stkpush_view(request):
    access_token = mpay_generate(request)  # Obtain the access token
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    callback_url = request.build_absolute_uri('/callbackurl/')  # Construct the callback URL dynamically

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwNTI0MjIyMDM2",
        "Timestamp": "20230524222036",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254705482738",
        "PartyB": 174379,
        "PhoneNumber": "254705482738",
        "CallBackURL": callback_url,  # Update the callback URL here
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    return HttpResponse(response.text, content_type='application/json')


import requests
import json

def check_transaction_status(transaction_id):
    access_token = mpay_generate()  # Obtain the access token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "Initiator": "testapi",
        "SecurityCredential": "PMHB2nskiUik2xRIfKOAsPYK7yUKY6RHwfRlu57PcFLTVhKqAMhSELjNnMoFC2FfoHbLhR7lx5Xy5xMXxBki+WuFjOeJ3rUl4uAH4OAvF7sVgqtYOhDM1T8jAUn3H7xy2jFJETWxSzqkcSRcnDYYoC+iW1RVUmdnB2sRUInk9eAZb2QEMVdOU1Efn/qdoZJ7lDS1Usb8cIbIQbq6LaRLogRWeSgPsyoHEPAomOffwtQAuosASMM0RHAQ7YfEUviWBuHrVzewdH/rVkTGKkPC7K4XbDuFVr0LYsrnJK7QJ4kQBzUOR5F0f9SXbvJ0wzIZPnOIL3nbKgk8S3kL7fGJpg==",
        "CommandID": "TransactionStatusQuery",
        "TransactionID": transaction_id,
        "PartyA": 600996,
        "IdentifierType": "2",
        "ResultURL": "https://mydomain.com/TransactionStatus/result/",
        "QueueTimeOutURL": "https://mydomain.com/TransactionStatus/queue/",
        "Remarks": "success",
        "Occassion": "success",
    }

    url = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query'

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = json.loads(response.text)

    # Process the response data
    originator_conversation_id = response_data.get("OriginatorConversationID")
    conversation_id = response_data.get("ConversationID")
    response_code = response_data.get("ResponseCode")
    response_description = response_data.get("ResponseDescription")

    # Do something with the response data
    print("Originator Conversation ID:", originator_conversation_id)
    print("Conversation ID:", conversation_id)
    print("Response Code:", response_code)
    print("Response Description:", response_description)

# Example usage
transaction_id = "OEI2AK4Q16"
check_transaction_status(transaction_id)



def c2b_view(request):
    headers = {
        'Authorization': 'Basic cFJZcjZ6anEwaThMMXp6d1FETUxwWkIzeVBDa2hNc2M6UmYyMkJmWm9nMHFRR2xWOQ=='
    }

    payload = {
        "ShortCode": 600983,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://mydomain.com/confirmation",
        "ValidationURL": "https://mydomain.com/validation"
    }

    return JsonResponse(payload)

