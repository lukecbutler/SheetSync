import gspread
from google.oauth2.service_account import Credentials

def write_to_sheet(workbook_id, transactions):
    """Writes a list of transactions to a specified Google Sheet."""
    try:
        print("Connecting to Google Sheets...")
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_key(workbook_id)
        sheet = workbook.worksheet('sheet1')
        print("✅ Connected to Google Sheet.")

        sheet_data = [['Date', 'Merchant Name', 'Amount']]
        for t in transactions:
            row = [
                str(t.date),
                t.merchant_name if t.merchant_name else 'N/A',
                t.amount
            ]
            sheet_data.append(row)
        
        sheet.clear()
        sheet.update('A1', sheet_data)
        print(f"🎉 Success! Wrote {len(sheet_data)} rows to the sheet.")
        return True
    except Exception as e:
        print(f"❌ Google Sheets Error: {e}")
        return False