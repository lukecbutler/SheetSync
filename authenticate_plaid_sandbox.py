import os
import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from dotenv import load_dotenv

# ==============================================================================
# Plaid Authenticator
# ------------------------------------------------------------------------------
# Description:
#   This script contains functions to handle each step of the Plaid
#   authentication flow and saves the final access token to a file.
# ==============================================================================

def configure_plaid_client():
    """
    Loads credentials and configures the Plaid client for the Sandbox.
    Returns:
        plaid_api.PlaidApi: An authenticated client object ready for use.
    """
    load_dotenv()
    client_id = os.getenv('PLAID_CLIENT_ID')
    secret = os.getenv('PLAID_SECRET')

    if not client_id or not secret:
        raise ValueError("PLAID_CLIENT_ID and PLAID_SECRET must be set in your .env file.")

    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={'clientId': client_id, 'secret': secret}
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def create_sandbox_public_token(client):
    """
    Creates a public_token for a test institution using a Sandbox-only function.
    Args:
        client (plaid_api.PlaidApi): The configured Plaid client.
    Returns:
        str: The generated public_token, or None on failure.
    """
    try:
        request = plaid_api.SandboxPublicTokenCreateRequest(
            institution_id='ins_109508',
            initial_products=[Products('transactions')]
        )
        response = client.sandbox_public_token_create(request)
        public_token = response['public_token']
        print("✅ Sandbox public_token created.")
        return public_token
    except plaid.ApiException as e:
        print(f"❌ Could not create public token: {e.body}")
        return None

def exchange_for_access_token(client, public_token):
    """
    Exchanges a public_token for a permanent access_token.
    Args:
        client (plaid_api.PlaidApi): The configured Plaid client.
        public_token (str): The one-time public token.
    Returns:
        str: The permanent access_token, or None on failure.
    """
    try:
        request = plaid_api.ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        access_token = response['access_token']
        print("✅ Access_token created.")
        return access_token
    except plaid.ApiException as e:
        print(f"❌ Could not exchange for access token: {e.body}")
        return None

def save_token(token, filename="access_token.txt"):
    """Saves a token to a specified file."""
    with open(filename, 'w') as f:
        f.write(token)
    print(f"\n🎉 Success! Token saved to {filename}")

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Starting Plaid Authentication ---")
    
    # 1. Set up the client to communicate with Plaid
    plaid_client = configure_plaid_client()
    
    # 2. Get the one-time public token (Sandbox shortcut)
    public_token = create_sandbox_public_token(plaid_client)
    
    # 3. If public token was created, exchange it for the permanent access token
    if public_token:
        access_token = exchange_for_access_token(plaid_client, public_token)
        
        # 4. If access token was created, save it to a file
        if access_token:
            save_token(access_token)