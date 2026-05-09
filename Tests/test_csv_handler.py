import unittest
import csv
import tempfile

from csv_handler import CSVHandler


class TestCSVHandler(unittest.TestCase):

    def setUp(self):
        self.handler = CSVHandler()

    # ---------------- File Not Found ----------------

    def test_load_vehicles_file_not_found(self):
        result = self.handler.load_vehicles("missing_vehicles.csv")
        self.assertEqual(result, [])

    def test_load_clients_file_not_found(self):
        result = self.handler.load_clients("missing_clients.csv", [])
        self.assertEqual(result, [])

    def test_load_workers_file_not_found(self):
        result = self.handler.load_workers("missing_workers.csv")
        self.assertEqual(result, [])

    def test_load_rentals_file_not_found(self):
        result = self.handler.load_rentals(
            "missing_rentals.csv",
            [],
            []
        )
        self.assertEqual(result, [])

    # ---------------- Truck Branch ----------------

    def test_load_truck_vehicle(self):
        with tempfile.NamedTemporaryFile(mode="w+", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "type",
                    "brand",
                    "color",
                    "license_plate",
                    "model",
                    "matriculation_date",
                    "mileage"
                ]
            )

            writer.writeheader()

            writer.writerow({
                "type": "Truck",
                "brand": "Scania",
                "color": "Grey",
                "license_plate": "4444DDD",
                "model": "R450",
                "matriculation_date": "2010-01-01",
                "mileage": "100000"
            })

            file.flush()

            vehicles = self.handler.load_vehicles(file.name)

            self.assertEqual(len(vehicles), 1)
            self.assertEqual(
                vehicles[0].license_plate,
                "4444DDD"
            )

    # ---------------- else: continue branch ----------------

    def test_unknown_vehicle_type_is_skipped(self):
        with tempfile.NamedTemporaryFile(mode="w+", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "type",
                    "brand",
                    "color",
                    "license_plate",
                    "model",
                    "matriculation_date",
                    "mileage"
                ]
            )

            writer.writeheader()

            writer.writerow({
                "type": "Plane",
                "brand": "Boeing",
                "color": "White",
                "license_plate": "9999ZZZ",
                "model": "747",
                "matriculation_date": "2010-01-01",
                "mileage": "10000"
            })

            file.flush()

            vehicles = self.handler.load_vehicles(file.name)

            self.assertEqual(vehicles, [])

if __name__ == "__main__":
    unittest.main()