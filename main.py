from datetime import date
from shop_manager import ShopManager
from car import Car
from motorbike import Motorbike
from truck import Truck
from client import Client
from admin import Admin


def menu():
    print("\n===== VEHICLE RENTAL SYSTEM =====")
    print("1. Add Vehicle")
    print("2. Add Client")
    print("3. Add Worker")
    print("4. Assign Vehicle to Client")
    print("5. Create Rental")
    print("6. View All Vehicles")
    print("7. View All Clients")
    print("8. View All Workers")
    print("9. View All Rentals")
    print("10. View Client Vehicles")
    print("11. Save and Exit")


def create_vehicle():
    print("\nVehicle Type:")
    print("1. Car")
    print("2. Motorbike")
    print("3. Truck")

    choice = input("Choose vehicle type: ")

    brand = input("Brand: ")
    color = input("Color: ")
    plate = input("License Plate: ")
    model = input("Model: ")

    year = int(input("Matriculation year: "))
    month = int(input("Matriculation month: "))
    day = int(input("Matriculation day: "))

    mileage = float(input("Mileage: "))

    matriculation_date = date(year, month, day)

    if choice == "1":
        return Car(brand, color, plate, model, matriculation_date, mileage)

    elif choice == "2":
        return Motorbike(
            brand,
            color,
            plate,
            model,
            matriculation_date,
            mileage
        )

    elif choice == "3":
        return Truck(
            brand,
            color,
            plate,
            model,
            matriculation_date,
            mileage
        )

    else:
        print("Invalid vehicle type.")
        return None


def create_client():
    name = input("Client name: ")

    year = int(input("Birth year: "))
    month = int(input("Birth month: "))
    day = int(input("Birth day: "))

    user_id = input("Client ID: ")

    dob = date(year, month, day)

    return Client(name, dob, user_id)


def create_worker():
    name = input("Worker name: ")

    year = int(input("Birth year: "))
    month = int(input("Birth month: "))
    day = int(input("Birth day: "))

    user_id = input("Worker ID: ")
    role = input("Role (mechanic/rental manager/administrator): ")

    dob = date(year, month, day)

    return Admin(name, dob, user_id, role)


def create_rental(manager):
    plate = input("Vehicle plate: ")
    client_id = input("Client ID: ")

    print("\nStart Date")
    start_year = int(input("Year: "))
    start_month = int(input("Month: "))
    start_day = int(input("Day: "))

    print("\nEnd Date")
    end_year = int(input("Year: "))
    end_month = int(input("Month: "))
    end_day = int(input("Day: "))

    kms_allowed = float(input("Allowed kms: "))
    insurance = input("Insurance (basic/premium/full): ")

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    manager.create_rental(
        plate,
        client_id,
        start_date,
        end_date,
        kms_allowed,
        insurance
    )

    print("Rental created successfully.")
def view_client_vehicles(manager):
    client_id = input("Client ID: ")
    client = manager.get_client(client_id)

    vehicles = client.vehicles

    if not vehicles:
        print("This client has no assigned vehicles.")
    else:
        print(f"\nVehicles assigned to {client.name}:")
        for vehicle in vehicles:
            print(vehicle)


def main():
    manager = ShopManager()

    while True:
        menu()

        choice = input("\nChoose an option: ")

        try:
            if choice == "1":
                vehicle = create_vehicle()

                if vehicle:
                    manager.add_vehicle(vehicle)
                    print("Vehicle added successfully.")

            elif choice == "2":
                client = create_client()
                manager.add_client(client)
                print("Client added successfully.")

            elif choice == "3":
                worker = create_worker()
                manager.add_worker(worker)
                print("Worker added successfully.")

            elif choice == "4":
                plate = input("Vehicle plate: ")
                client_id = input("Client ID: ")

                manager.assign_vehicle_to_client(
                    plate,
                    client_id
                )

                print("Vehicle assigned successfully.")

            elif choice == "5":
                create_rental(manager)

            elif choice == "6":
                vehicles = manager.get_all_vehicles()

                for vehicle in vehicles:
                    print(vehicle)

            elif choice == "7":
                clients = manager.get_all_clients()

                for client in clients:
                    print(client)

            elif choice == "8":
                workers = manager.get_all_workers()

                for worker in workers:
                    print(worker)

            elif choice == "9":
                rentals = manager.get_all_rentals()

                for rental in rentals:
                    print(rental)

            elif choice == "10":
                view_client_vehicles(manager)

            elif choice == "11":
                manager.save_all()
                print("Data saved successfully.")
                print("Goodbye.")
                break

            else:
                print("Invalid option.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()