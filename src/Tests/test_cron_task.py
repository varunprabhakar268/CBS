import mock
import pandas as pd
from src import CronTask
import matplotlib.pyplot as plt


class MockFigure:
    """Mock class for Figure."""

    def savefig(self, location):
        return True


class TestCronTask:

    @mock.patch('src.CronTask.pd.read_sql_query')
    def test_get_monthly_bookings(self, mock_read_sql_query):
        mock_read_sql_query.return_value = pd.DataFrame({'test': [1, 2, 3]})

        result = CronTask.get_monthly_bookings()

        mock_read_sql_query.assert_called_once()
        pd.testing.assert_frame_equal(result, pd.DataFrame({'test': [1, 2, 3]}))

    @mock.patch('src.CronTask.pd.read_sql_query')
    def test_get_daily_bookings(self, mock_read_sql_query):
        mock_read_sql_query.return_value = pd.DataFrame({'test': [1, 2, 3]})

        result = CronTask.get_daily_bookings()

        mock_read_sql_query.assert_called_once()
        pd.testing.assert_frame_equal(result, pd.DataFrame({'test': [1, 2, 3]}))

    @mock.patch('src.CronTask.pd.read_sql_query')
    def test_get_booking_destination(self, mock_read_sql_query):
        mock_read_sql_query.return_value = pd.DataFrame({'test': [1, 2, 3]})

        result = CronTask.get_booking_destination()

        mock_read_sql_query.assert_called_once()
        pd.testing.assert_frame_equal(result, pd.DataFrame({'test': [1, 2, 3]}))

    def test_plot_monthly_bookings_report(self):
        df = pd.DataFrame({'month': [1, 2, 3], 'total_bookings': [2, 2, 2]})

        num_figures_before = plt.gcf().number
        result = CronTask.plot_monthly_bookings_report(df)
        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after

    def test_plot_daily_bookings_report(self):
        df = pd.DataFrame({'date': [1, 2, 3], 'total_bookings': [2, 2, 2]})
        num_figures_before = plt.gcf().number

        result = CronTask.plot_daily_bookings_report(df)

        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after

    def test_plot_booking_destination_report(self):
        df = pd.DataFrame({'destination': [1, 2, 3], 'total_bookings': [2, 2, 2]})
        num_figures_before = plt.gcf().number

        result = CronTask.plot_booking_destination_report(df)

        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after

    @mock.patch('src.CronTask.plot_monthly_bookings_report')
    @mock.patch('src.CronTask.get_monthly_bookings')
    def test_create_monthly_bookings_report(self, mock_get_monthly_bookings,
                                            mock_plot_monthly_bookings_report):
        mock_get_monthly_bookings.return_value = pd.DataFrame({'test': [1, 2, 3]})

        mock_plot_monthly_bookings_report.return_value = MockFigure()

        result = CronTask.create_monthly_bookings_report()

        assert result is True

    @mock.patch('src.CronTask.plot_daily_bookings_report')
    @mock.patch('src.CronTask.get_daily_bookings')
    def test_create_daily_bookings_report(self, mock_get_daily_bookings,
                                          mock_plot_daily_bookings_report):
        mock_get_daily_bookings.return_value = pd.DataFrame({'test': [1, 2, 3]})

        mock_plot_daily_bookings_report.return_value = MockFigure()

        result = CronTask.create_daily_bookings_report()

        assert result is True

    @mock.patch('src.CronTask.plot_booking_destination_report')
    @mock.patch('src.CronTask.get_booking_destination')
    def test_create_booking_destination_report(self, mock_get_booking_destination,
                                               mock_plot_booking_destination_report):
        mock_get_booking_destination.return_value = pd.DataFrame({'test': [1, 2, 3]})

        mock_plot_booking_destination_report.return_value = MockFigure()

        result = CronTask.create_booking_destination_report()

        assert result is True
