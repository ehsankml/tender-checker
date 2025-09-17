import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# آدرس فید RSS
URL = "https://www.parsnamaddata.com/rss"

# کلیدواژه‌ها برای فیلتر کردن
KEYWORDS = ["عمرانی", "راه", "پل", "ساختمان", "پروژه", "بتن", "بتن‌ریزی", "سازه", "عمران"]

def get_tenders():
    feed = feedparser.parse(URL)
    tenders = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        if any(keyword in title for keyword in KEYWORDS):
            tenders.append({"title": title, "link": link})
    return tenders

def send_email(tenders):
    sender_email = os.environ["EMAIL_USER"]
    receiver_email = os.environ["EMAIL_TO"]
    password = os.environ["EMAIL_PASS"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📢 گزارش روزانه مناقصه‌های عمرانی (RSS)"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    if tenders:
        html_content = "<h3>📌 مناقصه‌های عمرانی امروز:</h3><ul>"
        for t in tenders:
            html_content += f"<li><a href='{t['link']}'>{t['title']}</a></li>"
        html_content += "</ul>"
    else:
        html_content = "<p>امروز مناقصه عمرانی پیدا نشد.</p>"

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    tenders = get_tenders()
    send_email(tenders)
