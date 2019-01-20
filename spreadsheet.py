#  All the required libraries imported first for Google API
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

#  Working with Google drive and sheets API
scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']

#  Saved Google credientials as client_secret.json file saved in the same directory 
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Stocks Data Table').sheet1
result = sheet.get_all_records()


df = pd.DataFrame(result, columns = ['Company Name', 'Price', 'Price High', 'Price Low', 'Volume', 'Percentage Change'])


#  All the required libraries imported first for python's smtplib module.    
import smtplib
# Port = 587 using TLS encryption
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
email_address = input('What is your email address? ')
password = input('What is the password of the given email address?')
smtpObj.login(email_address, password)


#  For sending a fancy email using html instead of a plain email.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Stock Alert"
msg['From'] = email_address
msg['To'] = email_address 

# Create the body of the message (a plain-text and an HTML version). 
html = df.to_html()


# Record the MIME types of text/html.  
part2 = MIMEText(html, 'html') 

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

msg.attach(part2)
#####################################################   
################################################

# Now the google news scraping through rss    
# Importing beauutiful soup for html scraping through python   
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
 
# A loop for scraping top news for each stock in df  
news_string = ''    
for i in range(df.shape[0]):
    name = df.at[i, 'Company Name'].replace(' ', '+') 
    news_url="https://news.google.com/rss/search?q=" + name + "+shares"
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close() 
    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")

    # Print 5 news title, url and publish date for each stock.    
    a = 0
    for news in news_list:
        if a<5 and (a + 1)%5 == 0:
            news_string = news_string + " " + news.title.text + '\n' + news.link.text + '\n' + news.pubDate.text
            news_string = news_string + '\n'*3 
        elif a <5:
            news_string = news_string + " " + news.title.text + '\n' + news.link.text + '\n' + news.pubDate.text
            news_string = news_string + "-"*60 + '\n'   
        a+=1


from jinja2 import Environment        # Jinja2 templating

TEMPLATE = """
<html>
<head>
<title>Stock Update</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

</head>
<body>

    <div class="container p-3 mb-2 bg-success text-white">
        <h1 class = "text-center">Stock Movement</h1>   
    {{table}}

    {{newsletter}}
    </div>

</body>
</html>
"""  # Our HTML Template

# Create a text/html message from a rendered template
msg = MIMEText(
    Environment().from_string(TEMPLATE).render(
        table=html, newsletter=news_string), "html") 





smtpObj.sendmail(email_address, email_address, msg.as_string())

smtpObj.quit()

