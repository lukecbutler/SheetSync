# gspread docs:
# https://docs.gspread.org/en/v6.0.0/user-guide.html#creating-a-spreadsheet
# Writes to Google Sheets
# Library for interacting with sheet
import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
# Client to access different google sheets
client = gspread.authorize(creds)

# Access to the specific google sheet - sheet_id found in the url between d & edit
sheet_id = "1hFtFiHxEF3TO7NU49Q3cbGrOpqWT_4fnnymNmqgWtzM"
# The main google sheet is 'workbook' ; 'worksheet' is the tab in the workbook
workbook = client.open_by_key(sheet_id)

values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
    ["Coffee", 3.99, 12]
]

# get the name of all of all sheets that exist
# gets all worksheet names insdie workbook
worksheetList = map(lambda x: x.title, workbook.worksheets())

# specify name of worksheet wanting to create
newWorksheetName = "Values"

# if the new name already exists in worksheets, set it to sheet
if newWorksheetName in worksheetList:
    sheet = workbook.worksheet(newWorksheetName)

# else: create it(name, number of rows & columns)
else:
    sheet = workbook.add_worksheet(newWorksheetName, rows=10, cols=10)

#removes everything inside of it - so we can start fresh
sheet.clear()

# update a range of cells at the same time, ex. if we have 4 rows, then we want to go to
# C4 - values is a list of lists
# also, pass in values to this update function
sheet.update(f"A1:C{len(values)}", values)

# add "Totals:" at bottom of filled rows
sheet.update_cell(len(values)+2, 1, "Total Price:")

# include total price
sheet.update_cell(len(values)+2, 2, "=sum(B2:B5)")




# Formatting Examples:
'''
sheet.format(f"A1:C{len(values)}", {'textFormat': {"bold": True}})
sheet.format(f"A2:C{len(values)}", {'textFormat': {"bold": False}})
'''

# Format specific cell in sheet
'''
sheet.format("A1",{"textFormat": {"bold": True}})
'''

# Find a cell by it's value
'''
sheet = workbook.worksheet('sheet1')
cell = sheet.find("boogabooga")
print(cell.row, cell.col)
'''

# Get value from specific cells
'''
sheet = workbook.worksheet("sheet1")
value = sheet.acell("A1").value
print(value)
'''

# Get sheet -> update_cell(row, column, data to add)
'''
sheet = workbook.worksheet("sheet1")
sheet.update_cell(1,1,"You added this with python!")
sheet.update_cell(2,1, "Let's see how far we can push this.")
'''

# Print out all titles of sheets
'''
sheets = map(lambda x: x.title, workbook.worksheets())
print(list(sheets))
'''