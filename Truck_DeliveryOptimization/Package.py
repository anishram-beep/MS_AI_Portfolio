class Package:
    all_packages = {}  # Global hash table for all packages

    def __init__(self, package_id, location, delivery_address="", delivery_deadline="",
                 delivery_city="", delivery_zipcode="", package_weight=""):
       if package_id != 0:
        self.package_id = package_id
        self.location = location
        self.status = "At Hub"
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zipcode = delivery_zipcode
        self.package_weight = package_weight
        self.delivery_time = None  # Track when package was delivered
        self.truck_departure_time = None  # New attribute
        Package.all_packages[package_id] = self  # Register package in hash table
       else :
           self.package_id = package_id
           self.location = location
           self.status = "At Hub"
           self.delivery_address = delivery_address
           self.delivery_deadline = delivery_deadline
           self.delivery_city = delivery_city
           self.delivery_zipcode = delivery_zipcode
           self.package_weight = package_weight
           self.delivery_time = None  # Track when package was delivered
           self.truck_departure_time = None  # New attribute
           Package.all_packages[package_id] = self  # Register package in hash table


    def mark_delivered(self, delivery_time):
        """Marks the package as delivered and records the delivery time."""
        self.status = "delivered"
        self.delivery_time = delivery_time

    def update_info(self, delivery_address=None, delivery_deadline=None, delivery_city=None,
                    delivery_zipcode=None, package_weight=None):
        """Updates the package details."""
        if delivery_address:
            self.delivery_address = delivery_address
        if delivery_deadline:
            self.delivery_deadline = delivery_deadline
        if delivery_city:
            self.delivery_city = delivery_city
        if delivery_zipcode:
            self.delivery_zipcode = delivery_zipcode
        if package_weight:
            self.package_weight = package_weight

    @classmethod
    def get_package(cls, package_id):
        """Retrieves a package instance by package ID."""
        return cls.all_packages.get(package_id)

    def info(self):
        """Returns a string representation of the package details."""
        return (f"Package({self.package_id}, Status: {self.status}, Delivery Time: {self.delivery_time}, "
                f"Address: {self.delivery_address}, State: {self.location}, Deadline: {self.delivery_deadline}), Package_Weight(KG): {self.package_weight})")
