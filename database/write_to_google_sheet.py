import logging
import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

WRITE_RANGE_NAME = "Статистика бот"
READ_RANGE_NAME = "Реєстрації весна 2026"

logger = logging.getLogger("UserActivity")


def get_spreadsheet_id() -> str:
    with open("spreadsheet_id.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


def write_to_google_sheet(data: list):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Sheets API
    service = build("sheets", "v4", credentials=creds)

    values = [data]
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=get_spreadsheet_id(),
            range=WRITE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )
    print(f"{result.get("updates").get('updatedCells')} cells updated.")
    return result
  except HttpError as err:
    print(err)


def read_from_google_sheet() -> pd.DataFrame:
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Sheets API
    service = build("sheets", "v4", credentials=creds)

    values = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=get_spreadsheet_id(),
            range=READ_RANGE_NAME,
        )
        .execute()
    ).get("values", [])

    if not values: 
      logger.info("No data found at spreadsheet")
      return pd.DataFrame()

    headers = values[0]
    data = values[1:]
    return pd.DataFrame(data, columns=headers)

  except HttpError as err:
    print(err)
    return pd.DataFrame()


def write_one_cell(column: str, cell_number: int, value: str):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Sheets API
    service = build("sheets", "v4", credentials=creds)

    body = {"values": [[value]]}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=get_spreadsheet_id(),
            range=f"{READ_RANGE_NAME}!{column}{cell_number}",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )
  except HttpError as err:
    print(err)