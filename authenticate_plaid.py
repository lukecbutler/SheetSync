import os
import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from dotenv import load_dotenv

# ==============================================================================
# Plaid Authenticator
# ------------------------------------------------------------------------------
# Description:
#   This script performs a one-time authentication with the Plaid Sandbox
#   to generate a permanent access token for a test institution.
#
# Usage:
#   Run this script once to create the 'access_token.txt' file.
# ==============================================================================
def produceSandboxAccessToken():
    """
    Performs the one-time authentication to get and save an access_token.
    """
    print("--- Starting Plaid Authentication ---")
    
    # Configure the Plaid client & secret in environment variables
    load_dotenv()

    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')

    # create configuration object to create client to speak to API
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={'clientId': PLAID_CLIENT_ID, 'secret': PLAID_SECRET}
    )
    api_client = plaid.ApiClient(configuration)
    # make client that will respond to requests
    client = plaid_api.PlaidApi(api_client)

    try:
        # Sandbox request and response skips over link token, that is used to link actual bank account
        # Create a sandbox public_token --- One products type is 'transactions' -> there are others
        sandbox_request = plaid_api.SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')]
        )
        sandbox_response = client.sandbox_public_token_create(sandbox_request)
        #--- Create Public Token ---
        # used as a one time token to retrieve access token
        public_token = sandbox_response['public_token']
        print("✅ Sandbox public_token created.")

        # Exchange public_token for an access_token
        exchange_request = plaid_api.ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        
        #--- Create Access Token ---
        # used as permanent bank account information access
        access_token = exchange_response['access_token']
        print("✅ Access_token created.")

        # Save the access_token to a file
        # access token will be used in pulling bank account transaction data
        with open('access_token.txt', 'w') as f:
            f.write(access_token)
        
        print("\n🎉 Success! Access token saved to access_token.txt")

    except plaid.ApiException as e:
        print(f"❌ An error occurred: {e.body}")

# run function only if running this file
if __name__ == "__main__":
    produceSandboxAccessToken()