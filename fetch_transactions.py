import os
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest
# import dotenv file so no one steals my key
from dotenv import load_dotenv


"""
Initializes and returns a Plaid client configured for the Sandbox.

This function reads the PLAID_CLIENT_ID and PLAID_SECRET from environment
variables to authenticate and prepares the client object for making API calls.
"""
def configureClient():

    # get client ID and secret for talking to API
    load_dotenv()
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={'clientId': PLAID_CLIENT_ID, 'secret': PLAID_SECRET}
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    return client



"""
Fetches new transactions from Plaid using a stored access token.

This function initializes a Plaid client, reads an access_token from
'access_token.txt', and retrieves a list of newly added transactions
from the /transactions/sync endpoint. It prints error messages if the
token file is missing or if there's an API error.

Returns:
    list: A list of transaction objects, or None if an error occurs.
""" 
def getTransactions():


    client = configureClient()
    try:
        # Read the access_token from the file
        with open('access_token.txt', 'r') as file:
            access_token = file.read()

        # Prepare the request to get transactions
        request = TransactionsSyncRequest(access_token=access_token)
        response = client.transactions_sync(request)
        transactions = response['added']
        '''
        for t in transactions:
            print("---")
            print(f"      Name: {t['merchant_name']}")
            print(f"    Amount: ${t['amount']:.2f}")
            print(f"      Date: {t['date']}")
        '''
        return transactions
    except FileNotFoundError:
        print("❌ access_token.txt not found. Please run authenticate_plaid.py first.")
    except plaid.ApiException as e:
        print(f"❌ An error occurred: {e.body}")