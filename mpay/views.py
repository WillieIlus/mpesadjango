import base64
import json
from datetime import datetime
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth


now = datetime.now()
consumer_key = 'lOIGknrirnapyrzdKp5VavouJ6ABy0RR'
consumer_secret = 'bMV32BQqTemWtGHA'
timestamp = now.strftime("%Y%m%d%H%M%S")
shortcode = 174379
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
checkout_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
transaction_status_url = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query'


def generate_password():
    password_str = str(shortcode) + str(pass_key) + str(timestamp)
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")


def get_access_token(request):
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


def mpesa_express(request):
    access_token = get_access_token(request)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": generate_password(),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254705482738",
        "PartyB": shortcode,
        "PhoneNumber": "254705482738",
        "CallBackURL": "https://mydomain.com/stkpush/callback/",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(checkout_url, headers=headers, json=payload)
    response_data = response.json()

    transaction_id = response_data.get('CheckoutRequestID')

    return JsonResponse(response_data)


def check_transaction_status(request):
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    transaction_id = "<your_transaction_id>"  # Replace with the actual transaction ID you want to check

    payload = {
        "BusinessShortCode": shortcode,
        "Password": generate_password(),
        "Timestamp": timestamp,
        "TransactionType": "TransactionStatusQuery",
        "TransactionID": transaction_id,
        "PartyA": "<your_phone_number>",
        "IdentifierType": "4",
        "ResultURL": "<your_callback_url>",
        "QueueTimeOutURL": "<your_timeout_callback_url>",
        "Remarks": "Transaction status check"
    }

    response = requests.post(transaction_status_url, headers=headers, json=payload)
    response_data = response.json()

    return JsonResponse(response_data)


def callback_view(request):
    print(request.body)  # Print the request body to inspect the received data
    callback_data = json.loads(request.body)
    transaction_id = callback_data['TransactionID']

    # Process the callback data and update your system accordingly

    return HttpResponse()

# import base64
# import json
# from datetime import datetime
# import requests
# from django.http import HttpResponse, JsonResponse
# from requests.auth import HTTPBasicAuth


# now = datetime.now()
# consumer_key = 'lOIGknrirnapyrzdKp5VavouJ6ABy0RR'
# consumer_secret = 'bMV32BQqTemWtGHA'
# timestamp = now.strftime("%Y%m%d%H%M%S")
# shortcode = 174379
# pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
# access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
# # access_token = None
# access_token_expiration = None
# checkout_url = None


# def generate_password():
#     password_str = str(shortcode) + str(pass_key) + str(timestamp)
#     password_bytes = password_str.encode("ascii")
#     return base64.b64encode(password_bytes).decode("utf-8")


# def get_access_token(request):
#     response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(response.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#     return validated_mpesa_access_token


# # def mpesaexpress(request):
# #     url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
# #     access_token = get_access_token(request)
# #     headers = {
# #         'Content-Type': 'application/json',
# #         'Authorization': 'Bearer %s' % access_token
# #     }
# #
# #     payload = {
# #         "BusinessShortCode": shortcode,
# #         "Password": generate_password(),
# #         "Timestamp": timestamp,
# #         "TransactionType": "CustomerPayBillOnline",
# #         "Amount": 1,
# #         "PartyA": "254705482738",
# #         "PartyB": shortcode,
# #         "PhoneNumber": "254705482738",
# #         "CallBackURL": "https://mydomain.com/path",
# #         "AccountReference": "CompanyXLTD",
# #         "TransactionDesc": "Payment of X"
# #     }
# #
# #     response = requests.post(url, headers=headers, json=payload)
# #     print(response.text.encode('utf8'))
# #     return HttpResponse(response)


# def mpesaexpress(request):
#     url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#     access_token = get_access_token(request)
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer %s' % access_token
#     }

#     payload = {
#         "BusinessShortCode": shortcode,
#         "Password": generate_password(),
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 1,
#         "PartyA": "254705482738",
#         "PartyB": shortcode,
#         "PhoneNumber": "254705482738",
#         "CallBackURL": "https://mydomain.com/stkpushquery/",
#         "AccountReference": "CompanyXLTD",
#         "TransactionDesc": "Payment of X"
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     print(response.text.encode('utf8'))
#     return response.json()  # Return JSON response directly


# def check_transaction_status(request):
#     url = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query'
#     access_token = get_access_token(request)
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer %s' % access_token
#     }

#     transaction_id = "<your_transaction_id>"  # Replace with the actual transaction ID you want to check

#     payload = {
#         "BusinessShortCode": shortcode,
#         "Password": generate_password(),
#         "Timestamp": timestamp,
#         "TransactionType": "TransactionStatusQuery",
#         "TransactionID": transaction_id,
#         "PartyA": "<your_phone_number>",
#         "IdentifierType": "4",
#         "ResultURL": "<your_callback_url>",
#         "QueueTimeOutURL": "<your_timeout_callback_url>",
#         "Remarks": "Transaction status check"
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     print(response.text.encode('utf8'))
#     return JsonResponse(response.json())


import base64
import json
from datetime import datetime
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth


now = datetime.now()
consumer_key = 'lOIGknrirnapyrzdKp5VavouJ6ABy0RR'
consumer_secret = 'bMV32BQqTemWtGHA'
timestamp = now.strftime("%Y%m%d%H%M%S")
shortcode = 174379
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
checkout_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
transaction_status_url = 'https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query'


def generate_password():
    password_str = str(shortcode) + str(pass_key) + str(timestamp)
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")


def get_access_token():
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return validated_mpesa_access_token


def mpesa_express(request):
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": generate_password(),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254705482738",
        "PartyB": shortcode,
        "PhoneNumber": "254705482738",
        "CallBackURL": "https://mydomain.com/stkpush/callback/",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(checkout_url, headers=headers, json=payload)
    response_data = response.json()

    transaction_id = response_data.get('CheckoutRequestID')

    return JsonResponse(response_data)


def check_transaction_status(request):
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    transaction_id = "<your_transaction_id>"  # Replace with the actual transaction ID you want to check

    payload = {
        "BusinessShortCode": shortcode,
        "Password": generate_password(),
        "Timestamp": timestamp,
        "TransactionType": "TransactionStatusQuery",
        "TransactionID": transaction_id,
        "PartyA": "<your_phone_number>",
        "IdentifierType": "4",
        "ResultURL": "<your_callback_url>",
        "QueueTimeOutURL": "<your_timeout_callback_url>",
        "Remarks": "Transaction status check"
    }

    response = requests.post(transaction_status_url, headers=headers, json=payload)
    response_data = response.json()

    return JsonResponse(response_data)


def callback_view(request):
    callback_data = json.loads(request.body)
    transaction_id = callback_data['TransactionID']

    # Process the callback data and update your system accordingly

    return HttpResponse()
