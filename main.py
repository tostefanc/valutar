#!/usr/bin/env python3

import smtplib
import ssl
import sec  # Local secrets
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs
import requests

r = requests.get("https://convertor-valutare.ro/curs-valutar-banci")


soup = bs(r.text, 'html.parser')
table_currency = soup.find(id="tabelBankValute")


def find_average_value_vanzare():
    nr_banci = len(table_currency.tbody.find_all('th'))
    valori_vanzare_raw = table_currency.tbody.select("tr > td:nth-of-type(3)")
    total_valori_vanzare = 0

    for valoare in valori_vanzare_raw:
        # print(float(valoare.text))
        total_valori_vanzare += float(valoare.text)

    return round(total_valori_vanzare / nr_banci, 2)


def find_average_value_cumparare():
    nr_banci = len(table_currency.tbody.find_all('th'))
    valori_vanzare_raw = table_currency.tbody.select("tr > td:nth-of-type(2)")
    total_valori_vanzare = 0

    for valoare in valori_vanzare_raw:
        # print(float(valoare.text))
        total_valori_vanzare += float(valoare.text)

    return round(total_valori_vanzare / nr_banci, 2)


htmlBody = f"""
<br/>
<h3> Media vanzare: {find_average_value_vanzare()} </h3>
<h3> Media cumparare: {find_average_value_cumparare()} </h3>
<br/>
<table class="column" style="border-spacing:0;width:100%;max-width:500px;vertical-align:top;display:inline-block;">
{table_currency.thead}
{table_currency.tbody}
<table/>
"""


today_date = dt.today().strftime('%d-%m-%Y')
subject_of_email = f'Curs valutar: {today_date}'


def all_receivers():
    if type(sec.email_receiver) is list:
        receivers = ', '.join(sec.email_receiver)
    else:
        receivers = sec.email_receiver
    return receivers


def send_the_lobster_articles(body_contents):
    em = MIMEMultipart()
    em['From'] = sec.email_sender
    em['To'] = all_receivers()
    em['Subject'] = subject_of_email
    em.attach(MIMEText(body_contents, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sec.email_sender, sec.email_sender_password)
        smtp.sendmail(sec.email_sender, sec.email_receiver, em.as_string())


send_the_lobster_articles(htmlBody)

