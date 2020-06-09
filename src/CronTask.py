import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import sqlite3


def create_monthly_bookings_report():
    conn = sqlite3.connect('/home/nineleaps/PythonAssignments/CBS/src/cbs_db.sqlite')
    sql = """select strftime('%m',date(created_at)) as 'Month',count(*) as 'TotalBookings' from bookings 
             where cancelled = 'no' 
             group by strftime('%m',date(created_at))"""
    monthly_booking_df = pd.read_sql_query(sql, conn)
    plot = monthly_booking_df.plot.bar(x='Month', y='TotalBookings', rot=0)
    fig = plot.get_figure()
    fig.savefig("MonthlyBookings.pdf")


def send_email():
    subject = "Cab Booking Details"
    body = "Please find the Cab Bookings Report attached with this email."
    sender_email = "testcronjob268@gmail.com"
    receiver_email = "captaincold268@gmail.com"
    password = ""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    filename = "MonthlyBookings.pdf"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


create_monthly_bookings_report()
send_email()
