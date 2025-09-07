import gspread
from google.oauth2.service_account import Credentials
from fetch_transactions import getTransactions

""" Initialize Requirements """
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
workbook_id = "1hFtFiHxEF3TO7NU49Q3cbGrOpqWT_4fnnymNmqgWtzM"
workbook = client.open_by_key(workbook_id)
sheet = workbook.worksheet('sheet1') #worksheet in google sheets

# Get transactions from the false account
transactions = getTransactions()

######################################################################################

def printFullTransactions():
    print(transactions)

#Set Merchant Name in First Row (A1)
def setMerchantName():
    sheet.update_cell(1,1, "Merchant Name")

#Set Amount in Second Row (B1)
def setAmount():
    sheet.update_cell(1,2, "Amount")

#Set Date in Third Row (C1)
def setDate():
    sheet.update_cell(1,3, "Date")

'''
Set Merchant Names in First Row (A2)
#1. Format List of Lists for Merchants
#2. Update Sheet starting at A2 with List of Lists
'''
def setMerchantNamesInSheet(transactions):
    merchants = []
    for t in transactions:
        merchants.append([t.merchant_name])
    sheet.update('A2', merchants)

'''
Set Amount in Second Row (B2)
#1. Format List of Lists for Amounts
#2. Update Sheet starting at B2 with Lists of Lists
'''
def setAmountsInSheet(transations):
    amounts = []
    for t in transactions:
        amounts.append([t.amount])
    sheet.update('B2', amounts)

'''
Set Date in Third Row (C2)
#1. Format List of Lists for Date
#2. Update Sheet starting at C2 with Lists of Lists
'''
def setDatesInSheet(transactions):
    dates = []
    for t in transactions:
        dates.append([str(t.date)])
    sheet.update('C2', dates)


def main():
    setMerchantNamesInSheet(transactions)
    setAmountsInSheet(transactions)
    setDatesInSheet(transactions)

main()

#example prints
"""    
print(f"      Name: {t.merchant_name}")
print(f"    Amount: ${t.amount:.2f}")
print(f"      Date: {t.date}")
"""