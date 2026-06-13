
import requests
from bs4 import BeautifulSoup
import smtplib
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

news_sources = [
    {
        "name": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml"
    },
    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/news/national/feeder/default.rss"
    },
    {
        "name": "Indian Express",
        "url": "https://indianexpress.com/section/india/feed/"
    }
]

all_news = []

for source in news_sources:
    print(f"Fetching news from {source['name']}...")

    response = requests.get(source["url"])
    soup = BeautifulSoup(response.text, "xml")

    items = soup.find_all("item")

    for item in items[:5]:
        title = item.find("title").get_text(strip=True)
        link = item.find("link").get_text(strip=True)
        pub_date = item.find("pubDate").get_text(strip=True)

        all_news.append({
            "source": source["name"],
            "title": title,
            "link": link,
            "time": pub_date
        })

print("\nTop News Headlines:\n")

for news in all_news:
    print("Source:", news["source"])
    print("Title:", news["title"])
    print("Link:", news["link"])
    print("Time:", news["time"])
    print("-" * 50)
    html_content = """
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #333333;
            text-align: center;
        }
        .news-item {
            border-bottom: 1px solid #dddddd;
            padding: 15px 0;
        }
        .source {
            color: #0066cc;
            font-weight: bold;
        }
        .title {
            font-size: 18px;
            margin: 5px 0;
        }
        .time {
            color: gray;
            font-size: 14px;
        }
        a {
            color: #cc0000;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Daily Top News Headlines</h1>
"""

for news in all_news:
    html_content += f"""
        <div class="news-item">
            <div class="source">{news['source']}</div>
            <div class="title">{news['title']}</div>
            <div class="time">{news['time']}</div>
            <a href="{news['link']}">Read more</a>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

with open("news_email.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML email file created successfully!")
sender_email = os.environ["SENDER_EMAIL"]
receiver_email = os.environ["RECIEVER_EMAIL"]
app_password = os.environ["APP_PASSWORD"]
if not sender_email or not reciever_email or not app_password:
    raise ValueError("One or more Github secrets are missing")

message = MIMEMultipart("alternative")
message["Subject"] = "Daily Top News Headlines - " + datetime.now().strftime("%d-%m-%Y %H:%M")
message["From"] = sender_email
message["To"] = receiver_email

html_part = MIMEText(html_content, "html")
message.attach(html_part)
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    print("Email sent successfully!")

except Exception as e:
    print("Email sending failed.")
    print(e)
    raise