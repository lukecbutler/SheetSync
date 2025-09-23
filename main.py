# Import the functions from your other modules
from plaid_client import configure_plaid_client, fetch_transactions
from sheets_client import write_to_sheet

def main():
    """
    Main function to orchestrate fetching Plaid transactions and syncing to Google Sheets.
    """
    # --- CONFIGURATION ---
    # The access_token for the Sandbox item you want to query
    sandbox_access_token = "access-sandbox-0bd533d0-1baa-4345-92a1-13da2e49e70b"
    # The ID of the Google Sheet you want to write to
    google_sheet_workbook_id = "1hFtFiHxEF3TO7NU49Q3cbGrOpqWT_4fnnymNmqgWtzM"

    print("--- Starting Transaction Sync ---")
    
    # --- 1. CONFIGURE AND FETCH FROM PLAID ---
    plaid_client = configure_plaid_client()
    transactions_list = fetch_transactions(plaid_client, sandbox_access_token)
    
    if not transactions_list:
        print("No transactions found or an error occurred. Exiting.")
        return
        
    print(f"✅ Fetched {len(transactions_list)} transactions from Plaid.")
    
    # --- 2. WRITE TO GOOGLE SHEETS ---
    write_to_sheet(google_sheet_workbook_id, transactions_list)

if __name__ == "__main__":
    main()