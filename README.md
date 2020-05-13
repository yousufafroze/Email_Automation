# Market_Anomaly_Detector

**Idea**: 
To help investors be notified of potential capital gains opportunity in the stock market. 

**What**: 
Sends am email about the stocks whose prices have drastically fallen. Includes new's headline, link and source.

**How**:
It parses HTML from google new's for the stocks' most pertinent news.
HTML and CSS is used for email templating and a range of Google API's through Python. 


*Template of the email is as follows*
[link]([https://www.youtube.com/watch?v=MTl8djZFWE0](https://www.youtube.com/watch?v=MTl8djZFWE0))
> ![alt text](https://github.com/yousufafroze/Market_Anomaly_Detector/blob/master/Template.png)


*Email sent is as follows: (The listing of news has a bug)*
![alt text](https://github.com/yousufafroze/Market_Anomaly_Detector/blob/master/Email.png)



Additional Details:
Stocks are from the investors stock portfolio in the Google Sheets
Attaches top 5 news, sorted according to their popularity about the stocks. 
