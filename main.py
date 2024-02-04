#!/usr/bin/env python3

import smtplib
import ssl
import sec  # Local secrets
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as bs
import requests


def main():
    r = requests.get("https://convertor-valutare.ro/curs-valutar-banci")

    soup = bs(r.text, 'html.parser')
    table_currency = soup.find(id="tabelBankValute")

    def find_average_value_action(action):
        nr_banci = len(table_currency.tbody.find_all('th'))
        valori_vanzare_raw = table_currency.tbody.select(f"tr > td:nth-of-type({action})")
        total_valori_vanzare = 0

        for valoare in valori_vanzare_raw:
            total_valori_vanzare += float(valoare.text)

        return round(total_valori_vanzare / nr_banci, 2)

    def get_min_max_values(action):
        banks = table_currency.tbody.select(f"tr > td:nth-of-type(1)")
        valori_raw = table_currency.tbody.select(f"tr > td:nth-of-type({action})")
        maximum = float(valori_raw[0].text)
        minimum = float(valori_raw[0].text)
        bank_maximum = ""
        bank_minimum = ""

        for valoare in range(len(valori_raw)):
            if float(valori_raw[valoare].text) > maximum:
                maximum = float(valori_raw[valoare].text)
                bank_maximum = banks[valoare].text

            if float(valori_raw[valoare].text) < minimum:
                minimum = float(valori_raw[valoare].text)
                bank_minimum = banks[valoare].text

        return {
            'max_values':
            {
                'bank': bank_maximum,
                'value': maximum
            },
            'min_values':
            {
                'bank': bank_minimum,
                'value': minimum
            }}

    min_max_vanzare = get_min_max_values(3)
    min_max_cumparare = get_min_max_values(2)

    html_body = f"""
    
    <h2> Vanzare: </h2>
    <h4>&nbsp; &nbsp; Media vanzare: {find_average_value_action(3)} </h4>
    <h4>&nbsp; &nbsp;
        Valoarea maxima: {min_max_vanzare['max_values']['value']} 
        este la: 
        {min_max_vanzare['max_values']['bank']} 
    </h4>
    
    <h4>&nbsp; &nbsp;
        Valoarea minima: {min_max_vanzare['min_values']['value']} 
        este la: 
        {min_max_vanzare['min_values']['bank']} 
    </h4>
    <br/>
    
    <h2> Cumparare: </h2>
    <h4>&nbsp; &nbsp; Media cumparare: {find_average_value_action(2)} </h4>
    <h4>&nbsp; &nbsp;
        Valoarea maxima: {min_max_cumparare['max_values']['value']} 
        este la: 
        {min_max_cumparare['max_values']['bank']} 
    </h4>
    <h4>&nbsp; &nbsp; 
        Valoarea minima: {min_max_cumparare['min_values']['value']} 
        este la: 
        {min_max_cumparare['min_values']['bank']} 
    </h4>
    
    <br/>
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

    def send_the_email(body_contents):
        em = MIMEMultipart()
        em['From'] = sec.email_sender
        em['To'] = all_receivers()
        em['Subject'] = subject_of_email
        em.attach(MIMEText(body_contents, 'html'))

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sec.email_sender, sec.email_sender_password)
            smtp.sendmail(sec.email_sender, sec.email_receiver, em.as_string())

    send_the_email(html_body)


if __name__ == '__main__':
    main()
