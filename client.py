from user import User
from vehicle import Vehicle
from exceptions import VehicleNotFoundError, ClientAlreadyHasVehicleError

class Client(User):
    def __init__(self, name, date_of_birth, user_id):
        super().__init__(name, date_of_birth, user_id)
        self.__vehicles = []

    @property
    def vehicles(self):
        return list(self.__vehicles)

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle): #Checks if vehicle is a Vehicle object 
            raise TypeError("Only Vehicle objects can be added.")
        if vehicle in self.__vehicles:
            raise ClientAlreadyHasVehicleError(f"{vehicle.license_plate} already belongs to this client.")

        self.__vehicles.append(vehicle)

    def remove_vehicle(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        self.__vehicles.remove(vehicle)

    def _find_vehicle(self, license_plate):
        plate = license_plate.upper().strip() #formatting

        for vehicle in self.__vehicles:
            if vehicle.license_plate == plate:
                return vehicle
        else:
            raise VehicleNotFoundError(f"Vehicle {license_plate} not found.")

    def update_vehicle_mileage(self, license_plate, new_mileage):
        vehicle = self._find_vehicle(license_plate)
        vehicle.update_mileage(new_mileage)

    def update_vehicle_color(self, license_plate, new_color):
        vehicle = self._find_vehicle(license_plate)
        vehicle.update_color(new_color)

    def check_next_itv(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        return vehicle.next_itv()

    def check_next_maintenance(self, license_plate):
        vehicle = self._find_vehicle(license_plate)
        return vehicle.next_maintenance()

    def get_info(self):
        plates = [v.license_plate for v in self.__vehicles] #creates a list containing the license plates of all vehicles in self.__vehicles.

        return (
            f"Client | {self.name} | ID: {self.user_id} "
            f"| Vehicles: {plates}")

    def to_csv_row(self): #creates a method that converts the object into a dictionary
        row = super().to_csv_row() #calls the parent class (User) to_csv_row() method and gets its dictionary --> so that the child calss can add information
        row["vehicles"] = ";".join(v.license_plate for v in self.__vehicles) #creates one string with all the vehicle plates separated by ;
        return row