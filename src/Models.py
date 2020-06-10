class EmployeeModel:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.email = kwargs.get('email', None)
        self.password = kwargs.get('password', None)


class CabModel:
    def __init__(self, **kwargs):
        self.cab_number = kwargs.get('cab_number', None)
        self.capacity = kwargs.get('capacity', None)


class RouteModel:
    def __init__(self, **kwargs):
        self.route = kwargs.get('route', None)


class CabRouteModel:
    def __init__(self, **kwargs):
        self.cab_number = kwargs.get('cab_number', None)
        self.route_id = kwargs.get('route_id', None)
        self.stop_name = kwargs.get('stop_name', None)
        self.stop_stage = kwargs.get('stop_stage', None)
        self.seats_available = kwargs.get('seats_available', None)
        self.timings = kwargs.get('timings', None)


class BookingsModel:
    def __init__(self, **kwargs):
        self.emp_id = kwargs.get('emp_id', None)
        self.route_id = kwargs.get('route_id', None)
        self.cab_number = kwargs.get('cab_number', None)
        self.source = kwargs.get('source', None)
        self.destination = kwargs.get('destination', None)
        self.timings = kwargs.get('timings', None)
        self.cancelled = kwargs.get('cancelled', None)
        self.end_date = kwargs.get('end_date', None)
