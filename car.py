from datetime import date
from dateutil.relativedelta import relativedelta
from vehicle import Vehicle

class Car(Vehicle):
    
    def next_itv(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=4) #takes the vehicle’s matriculation date and adds 4 years to calculate the next ITV date.

        while next_date <= today:
            age = relativedelta(next_date, self.matriculation_date).years
            if age < 10:
                next_date += relativedelta(years=2)
            else:
                next_date += relativedelta(years=1)

        return next_date

    def next_maintenance(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=1) ##takes the vehicle’s matriculation date and adds 1 year to calculate the next maintenance date.

        while next_date <= today:
            next_date += relativedelta(years=1)

        return f"Next maintenance: {next_date}"