# google_sheets_api

## Setup

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

You need to activate Google Sheets API access via Google Cloud Console. Then put your `credentials.json` file into the working directory. When you run the script first time, `token.json` file will be automatically generated after browser authentication process.

## Run

`google_sheets_parse_dates.py`: parses the dates from the given column and writes parsed dates back to defined column in a google spreadsheet.

Before running DO NOT FORGET to change `spreadsheet_id` and `sheet_name` values inside `main()` function.

Finally, run:
```
$ python3 google_sheets_parse_dates.py
```

## More info

For more info, visit:
[https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)