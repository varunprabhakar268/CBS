from crontab import CronTab


def cron_job():
    my_cron = CronTab(user='nineleaps')
    job = my_cron.new(command='python3 /home/nineleaps/PythonAssignments/CBS/src/CronTask.py',
                      comment='send_booking_report')
    job.day.every(1)
    my_cron.write()
    return True


if __name__ == '__main__': \
    cron_job()
