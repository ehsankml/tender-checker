import feedparser
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# لینک‌های RSS صفحات مختلف
RSS_FEEDS = [
    "https://www.parsnamaddata.com/مناقصه-بتن-ریزی/rss",
    "https://www.parsnamaddata.com/مناقصات-راهسازی/rss"
]

def get_today_tenders():
    today = datetime.date.today()
    tenders = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.get("published_parsed")

            # تاریخ امروز؟
            if published:
                entry_date = datetime.date(
                    published.tm_year, published.tm_mon, published.tm_mday
                )
                if entry_date != today:
                    continue

            # استان آذربایجان شرقی؟
            if "آذربایجان شرقی" in title or "آذربایجان شرقی" in entry.get("summary", ""):
                tenders.append({"title": title, "link": link})
    return tenders

def send_email(tenders):
    sender_email = os.environ["EMAIL_USER"]
    receiver_email = os.environ["EMAIL_TO"]
    password = os.environ["EMAIL_PASS"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📢 مناقصه‌های امروز (آذربایجان شرقی)"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    if tenders:
        html_content = "<h3>📌 مناقصه‌های امروز در آذربایجان شرقی:</h3><ul>"
        for t in tenders:
            html_content += f"<li><a href='{t['link']}'>{t['title']}</a></li>"
        html_content += "</ul>"
    else:
        html_content = "<p>امروز مناقصه‌ای در آذربایجان شرقی پیدا نشد.</p>"

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    tenders = get_today_tenders()
    send_email(tenders)
