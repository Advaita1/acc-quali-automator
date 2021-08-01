# ACC Quali Automator

ACC Quali Automator is a python application that watches a folder for ACC session data and updates a Google Sheets spreadsheet with fastest laps of the session.

## Installation

```bash
pip3 install -r requirements.txt
```

## Setup

### Give ACC Quali Automator Access to Your Spreadsheet

1. Log into the Google account that owns your qualifying spreadsheet.
2. Follow steps 1-5 in this [article](https://medium.datadriveninvestor.com/use-google-sheets-as-your-database-using-python-77d40009860f).
3. From the service account page, click keys -> add key -> create new key -> JSON -> create.
4. Rename this key to auth.json and move it into /acc_quali_automation/
5. Continue following steps 6 and 7 in the article to give ACC Quali Automator access to your sheet.

### config.py

Taking the config.py.example file as your guide, create a file called config.py inside /acc_quali_automation/

```bash
FILE_PATH = 'YOUR FILE PATH HERE'
SPREADSHEET_NAME = 'YOUR SPREADSHEET NAME HERE'
```

FILE_PATH is the relative file path to the folder that the UTF-8 converted ACC session files will be created in.

SPREADSHEET_NAME is the name of the spreadsheet that stores the best times from your quali server.

### Sheet Expectations

ACC Quali Automator expects that your sheet has a header row with five columns:

#, DRIVER NAME, CAR, NUMBER, LAP TIME

The cells under # must be formatted as =rows() - 1

The application also expects that there will be no more than 500 records per sheet.

# Usage

Run the command

```bash
python3 app.py
```

# Limitations

At the moment ACC Qauli Automator does not handle the case where two separate drivers have the same first and last name. If you run into this case, a middle initial should be enforced to distinguish the drivers.

The application also does not handle the JSON files that are directly output from an ACC server. These files are UTF-16 encoded and must first be converted to UTF-8.