Setup
1. Environment
This project uses Python. It's recommended to use a virtual environment.

Bash:
python -m venv venv
source venv/bin/activate

2. Dependencies
Install the required Plaid library:

Bash:
pip install plaid

3. API Keys
This project requires API keys from a Plaid developer account. Set the following environment variables in your terminal session before running the scripts:

Bash:
export PLAID_CLIENT_ID='your_client_id_here'
export PLAID_SECRET='your_plaid_secret_here'

---------------------------------------------------------------------------
Usage!
The workflow is a two-step process:

Step 1: Authenticate (Run Once)
First, run the authentication script. This will connect to the Plaid Sandbox, generate a permanent access_token, and save it to a file named access_token.txt.

Step 2: Fetch Transactions (Run Anytime)
After the access_token.txt file has been created, run this script anytime you want to fetch new transactions. It reads the token from the file and pulls the latest transaction data from the Plaid Sandbox.