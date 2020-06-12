import os
import smtplib
import sqlite3
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

conn = sqlite3.connect('/home/nineleaps/PythonAssignments/CBS/cbs_db.sqlite')


def get_monthly_bookings():
    sql = """select strftime('%m',date(created_at)) as 'month',count(*) as 'total_bookings' from Bookings 
                 where cancelled = 'no' 
                 group by strftime('%m',date(created_at))"""
    monthly_booking_df = pd.read_sql_query(sql, conn)
    return monthly_booking_df


def plot_monthly_bookings_report(monthly_booking_df):
    plot = monthly_booking_df.plot.bar(x='month', y='total_bookings', rot=0)
    fig = plot.get_figure()
    return fig


def create_monthly_bookings_report():
    monthly_booking_df = get_monthly_bookings()
    fig = plot_monthly_bookings_report(monthly_booking_df)
    fig.savefig("../report/MonthlyBookings.pdf")
    return True


def get_daily_bookings():
    sql = "select date(created_at) as 'date',count(*) as 'total_bookings' from bookings where cancelled = 'no' group by date(created_at) limit 31"
    daily_booking_df = pd.read_sql_query(sql, conn)
    return daily_booking_df


def plot_daily_bookings_report(daily_booking_df):
    plot = daily_booking_df.plot.bar(x='date', y='total_bookings', rot=0)
    fig = plot.get_figure()
    return fig


def create_daily_bookings_report():
    daily_booking_df = get_daily_bookings()
    fig = plot_daily_bookings_report(daily_booking_df)
    fig.savefig("../report/DailyBookings.pdf")
    return True


def get_booking_destination():
    sql = "select destination ,count(*) as 'total_bookings' from bookings where cancelled = 'no' group by destination"
    destination_df = pd.read_sql_query(sql, conn)
    return destination_df


def plot_booking_destination_report(destination_df):
    plot = destination_df.plot.bar(x='destination', y='total_bookings', rot=0)
    fig = plot.get_figure()
    return fig


def create_booking_destination_report():
    destination_df = get_booking_destination()
    fig = plot_booking_destination_report(destination_df)
    fig.savefig("../report/Destination.pdf")
    return True


def send_email():
    dir_path = "../report"
    files = ['MonthlyBookings.pdf', 'DailyBookings.pdf', 'Destination.pdf']
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
    for file in files:
        file_path = os.path.join(dir_path, file)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=file)
        message.attach(attachment)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def cron_task():
    create_monthly_bookings_report()
    create_daily_bookings_report()
    create_booking_destination_report()
    send_email()


if __name__ == '__main__': \
    cron_task()
