from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta

from exceptions import InvalidLicensePlateError, InvalidMileageError, InvalidDateError

class Vehicle(ABC):
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        self.__brand = self.validate_text_field(brand, "Brand") #making sure only valid varaibles are initialized
        self.__color = self.validate_text_field(color, "Color")
        self.__license_plate = self.validate_license_plate(license_plate)
        self.__model = self.validate_text_field(model, "Model")
        self.__matriculation_date = self.validate_date(matriculation_date)
        self.__mileage = self.validate_mileage(mileage)

    @property #@property is used to access private attributes safely from outside the class.
    def brand(self):
        return self.__brand

    @property
    def color(self):
        return self.__color

    @property
    def license_plate(self):
        return self.__license_plate

    @property
    def model(self):
        return self.__model

    @property
    def matriculation_date(self):
        return self.__matriculation_date

    @property
    def mileage(self):
        return self.__mileage

#VALLIDATORS

    def validate_text_field(self, value, field_name): 
        if not isinstance(value, str): #checks that the value inputed is a string
            raise ValueError(f"{field_name} must be a string.")

        if value.strip() == "":  #checks that the value inputed is not empty
            raise ValueError(f"{field_name} cannot be empty.")
        
        return value.strip()

    def validate_license_plate(self, plate):
        if not isinstance(plate, str): #checks that the value inputed is a string
            raise InvalidLicensePlateError("License plate must be a string.")

        plate = plate.strip().upper() #formatting

        if len(plate) != 7: #Checks that the plate has exactly 7 characters
            raise InvalidLicensePlateError("License plate must have 7 characters.")
        if not plate[:4].isdigit(): #Checks that the first 4 characters are numbers.
            raise InvalidLicensePlateError("First 4 characters must be numbers.")
        if not plate[4:].isalpha(): #Checks that the last 3 characters are letters.
            raise InvalidLicensePlateError("Last 3 characters must be letters.")
        for letter in plate[4:]: #Checks that every letter is between A and Z.
            if letter < "A" or letter > "Z":
                raise InvalidLicensePlateError("Last 3 characters must be Spanish plate letters.")

        return plate

    def validate_mileage(self, mileage):
        if not isinstance(mileage, (int, float)): #Checks if mileage is a number, it allows inteers and floats
            raise InvalidMileageError("Mileage must be numeric.")
        if mileage < 0:
            raise InvalidMileageError("Mileage cannot be negative.")

        return float(mileage)

    def validate_date(self, matriculation_date):
        if not isinstance(matriculation_date, date): #checks if matriculation_date is really a date object.
            raise InvalidDateError("Matriculation date must be a date object.")
        if matriculation_date > date.today():
            raise InvalidDateError("Matriculation date cannot be in the future.")

        return matriculation_date

#UPDATE METHODS

    def update_brand(self, new_brand):
        self.__brand = self.validate_text_field(new_brand, "Brand")

    def update_color(self, new_color):
        self.__color = self.validate_text_field(new_color, "Color")

    def update_model(self, new_model):
        self.__model = self.validate_text_field(new_model, "Model")

    def update_mileage(self, new_mileage):
        new_mileage = self.validate_mileage(new_mileage)

        if new_mileage < self.__mileage:
            raise InvalidMileageError("Mileage cannot decrease.")

        self.__mileage = new_mileage

#OTHER METHODS

    def years_since_matriculation(self):
        return relativedelta(date.today(), self.__matriculation_date).years #Calculates the difference between the two dates (.years takes only the years)

    @abstractmethod
    def next_itv(self):  
        pass

    @abstractmethod
    def next_maintenance(self):  
        pass

    def to_csv_row(self):
        return {
            "type": self.__class__.__name__,
            "brand": self.brand,
            "color": self.color,
            "license_plate": self.license_plate,
            "model": self.model,
            "matriculation_date": self.matriculation_date.isoformat(),
            "mileage": self.mileage}

    def __eq__(self, other):
        if not isinstance(other, Vehicle): #This checks that the object being compared is actually a Vehicle
            return NotImplemented

        return self.license_plate == other.license_plate

    def __str__(self):
        return (
            f"{self.__class__.__name__} | "
            f"{self.brand} {self.model} | "
            f"Plate: {self.license_plate} | "
            f"Color: {self.color} | "
            f"Mileage: {self.mileage}")