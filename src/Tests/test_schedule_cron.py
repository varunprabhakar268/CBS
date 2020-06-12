import mock

from src.ScheduleCron import cron_job


class MockCronTab:
    def new(self,command, comment):
        return MockJob

    def write(self):
        return True


class MockJob:
        class day:
            def every(self):
                return True


class TestScheduleCron:

    @mock.patch('src.ScheduleCron.CronTab')
    def test_cron_job(self, mock_crontab):
        mock_crontab.return_value = MockCronTab()

        result = cron_job()

        assert result is True
