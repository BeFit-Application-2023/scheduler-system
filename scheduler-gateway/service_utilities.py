class Service:
    NAME = None
    PORT = None
    PATHS = []


class ServiceBuilder:

    def __init__(self, service_info) -> None:
        self.service_info = service_info
        self.service = Service()

    def get_service_name(self):
        self.service.NAME = self.service_info['service-name']

    def get_service_port(self):
        self.service.PORT = self.service_info['service-port']

    def get_service_endpoints(self):
        self.service.PATHS = self.service_info['service-endpoints']
    
    def get_service_obj(self):
        return self.service
    

class Director:
    "The Director, building a complex representation."
    def __init__(self):
        self.service_list = []

    def construct(self, service_info):
        "Constructs and returns the final product"
        self.service_list.append(ServiceBuilder(service_info)\
            .get_service_name()\
            .get_service_port()\
            .get_service_endpoints()\
            .get_service_obj())
