import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest

def configure_plaid_client():
    """Loads credentials and configures the Plaid client for Sandbox."""
    load_dotenv()
    client_id = os.getenv('PLAID_CLIENT_ID')
    secret = os.getenv('PLAID_SECRET')
    if not client_id or not secret:
        raise ValueError("PLAID_CLIENT_ID and PLAID_SECRET must be set in your .env file.")
    configuration = plaid.Configuration(
        host='https://sandbox.plaid.com',
        api_key={'clientId': client_id, 'secret': secret}
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def fetch_transactions(client, access_token):
    """Queries and returns transactions for a given access_token."""
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
        )
        response = client.transactions_get(request)
        return response['transactions']
    except plaid.ApiException as e:
        print(f"❌ Plaid API Error: {e.body}")
        return []