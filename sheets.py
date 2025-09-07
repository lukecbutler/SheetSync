# gspread docs:
# https://docs.gspread.org/en/v6.0.0/user-guide.html#creating-a-spreadsheet
#Writes to Google Sheets
#library for interacting with sheet
import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
# client to access different google sheets
client = gspread.authorize(creds)

#access to the specific google sheet - sheet_id found in the url between d & edit
sheet_id = "1hFtFiHxEF3TO7NU49Q3cbGrOpqWT_4fnnymNmqgWtzM"
# The main google sheet is 'workbook' ; 'worksheet' is the tab in the workbook
workbook = client.open_by_key(sheet_id)












# get sheet -> update_cell(row, column, data to add)
'''
sheet = workbook.worksheet("sheet1")
sheet.update_cell(1,1,"You added this with python!")
sheet.update_cell(2,1, "Let's see how far we can push this.")
sheet.update_cell(3,1, "It isn't about what you know, but about what you can do.")
'''

#print out all titles of sheets
#sheets = map(lambda x: x.title, workbook.worksheets())
#print(list(sheets))

