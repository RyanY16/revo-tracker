from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from pathlib import Path

def create_data():
    #setup, reference: https://python-forum.io/thread-34862.html
    options = Options()
    options.add_argument("--headless")

    datadir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(datadir, "chromedriver.exe")

    browser = webdriver.Chrome(executable_path=path, options=options)

    url = "https://revofitness.com.au/"
    browser.get(url)
    doc = BeautifulSoup(browser.page_source, "lxml")

    location = doc.find(id = "___-number") #changes location to be tracked
    count = int(location.get_text())

    now = datetime.datetime.now()
    timestamp = int(now.timestamp())
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M")
    day = now.strftime("%A")
    
    df_new = pd.DataFrame({"Timestamp": [timestamp], "Date": [date], "Time": [time], "Day": [day], "Member count": [count]})
    return df_new

def check_file():
  spreadsheet_datadir = os.path.dirname(os.path.abspath(__file__))
  spreadsheet_path = os.path.join(spreadsheet_datadir, "spreadsheet.csv")
  file = Path(spreadsheet_path)
  if file.is_file():
    return True
  return False

if not check_file():
  df = create_data()
  df.to_csv("spreadsheet.csv", index = False)

while True:
  time.sleep(10)
  df_original = pd.read_csv("spreadsheet.csv")
  df = df.iloc[:, 1:]
  new_data = create_data()
  df_original = pd.concat([df_original, new_data])
  df_original.to_csv("spreadsheet.csv", index = False)