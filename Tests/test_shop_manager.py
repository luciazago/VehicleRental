import unittest
from datetime import date
from dateutil.relativedelta import relativedelta

from shop_manager import ShopManager
from car import Car
from motorbike import Motorbike
from truck import Truck
from client import Client
from admin import Admin
from exceptions import (
    DuplicateLicensePlateError, DuplicateIDError,
    VehicleNotFoundError, UserNotFoundError,
    RentalNotFoundError, VehicleAlreadyRentedError
)


class TestShopManager(unittest.TestCase):

    def setUp(self):
        # Create a fresh shop and clear all lists
        # so tests don't depend on CSV files
        self.shop = ShopManager()
        self.shop._ShopManager__vehicles = []
        self.shop._ShopManager__clients = []
        self.shop._ShopManager__workers = []
        self.shop._ShopManager__rentals = []

        self.car = Car("Toyota", "Red", "1234ABC", "Corolla", date(2015, 1, 1), 50000)
        self.car2 = Car("BMW", "Blue", "5678DEF", "Series3", date(2018, 1, 1), 30000)
        self.motorbike = Motorbike("Honda", "Black", "3333CCC", "CBR", date(2019, 1, 1), 10000)
        self.truck = Truck("Volvo", "White", "4444DDD", "FH16", date(2010, 1, 1), 100000)
        self.client = Client("Anna Smith", date(1990, 1, 1), "C001")
        self.client2 = Client("Bob Jones", date(1985, 1, 1), "C002")
        self.admin = Admin("Carlos", date(1975, 1, 1), "A001", "mechanic")
        self.admin2 = Admin("Diana", date(1978, 1, 1), "A002", "administrator")

        self.today = date.today()
        self.start = self.today - relativedelta(days=3)
        self.end = self.today + relativedelta(days=7)
        self.past_start = self.today - relativedelta(days=10)
        self.past_end = self.today - relativedelta(days=1)
        self.future_start = self.today + relativedelta(days=2)
        self.future_end = self.today + relativedelta(days=10)

    def tearDown(self):
        pass

    # ── Vehicles ──────────────────────────────────────────────────────────────

    def test_add_vehicle(self):
        self.shop.add_vehicle(self.car)
        self.assertIn(self.car, self.shop.get_all_vehicles())

    def test_add_multiple_vehicles(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.assertEqual(len(self.shop.get_all_vehicles()), 2)

    def test_add_duplicate_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)
        with self.assertRaises(DuplicateLicensePlateError):
            self.shop.add_vehicle(self.car)

    def test_get_vehicle(self):
        self.shop.add_vehicle(self.car)
        result = self.shop.get_vehicle("1234ABC")
        self.assertEqual(result, self.car)

    def test_get_vehicle_case_insensitive(self):
        self.shop.add_vehicle(self.car)
        result = self.shop.get_vehicle("1234abc")
        self.assertEqual(result, self.car)

    def test_get_vehicle_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.get_vehicle("9999ZZZ")

    def test_remove_vehicle(self):
        self.shop.add_vehicle(self.car)
        self.shop.remove_vehicle("1234ABC")
        self.assertNotIn(self.car, self.shop.get_all_vehicles())

    def test_remove_vehicle_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.remove_vehicle("9999ZZZ")

    def test_remove_active_rented_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_vehicle("1234ABC")

    def test_remove_upcoming_rented_vehicle_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.future_start, self.future_end, 500, "basic"
        )
        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_vehicle("1234ABC")

    def test_remove_vehicle_with_finished_rental_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.past_start, self.past_end, 500, "basic"
        )
        self.shop.remove_vehicle("1234ABC")
        self.assertNotIn(self.car, self.shop.get_all_vehicles())

    def test_get_all_vehicles_returns_copy(self):
        self.shop.add_vehicle(self.car)
        vehicles = self.shop.get_all_vehicles()
        vehicles.clear()
        self.assertEqual(len(self.shop.get_all_vehicles()), 1)

    def test_update_vehicle_color(self):
        self.shop.add_vehicle(self.car)
        self.shop.update_vehicle_color("1234ABC", "Green")
        self.assertEqual(self.car.color, "Green")

    def test_update_vehicle_color_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.update_vehicle_color("9999ZZZ", "Green")

    def test_update_vehicle_mileage(self):
        self.shop.add_vehicle(self.car)
        self.shop.update_vehicle_mileage("1234ABC", 60000)
        self.assertEqual(self.car.mileage, 60000)

    def test_update_vehicle_mileage_not_found_raises_error(self):
        with self.assertRaises(VehicleNotFoundError):
            self.shop.update_vehicle_mileage("9999ZZZ", 60000)

    def test_check_vehicle_itv(self):
        self.shop.add_vehicle(self.car)
        itv = self.shop.check_vehicle_itv("1234ABC")
        self.assertGreater(itv, date.today())

    def test_check_vehicle_maintenance(self):
        self.shop.add_vehicle(self.car)
        result = self.shop.check_vehicle_maintenance("1234ABC")
        self.assertIn("Next maintenance", result)

    def test_different_vehicle_types_added(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.motorbike)
        self.shop.add_vehicle(self.truck)
        self.assertEqual(len(self.shop.get_all_vehicles()), 3)

    # ── Clients ───────────────────────────────────────────────────────────────

    def test_add_client(self):
        self.shop.add_client(self.client)
        self.assertIn(self.client, self.shop.get_all_clients())

    def test_add_duplicate_client_raises_error(self):
        self.shop.add_client(self.client)
        with self.assertRaises(DuplicateIDError):
            self.shop.add_client(self.client)

    def test_add_client_same_id_as_worker_raises_error(self):
        self.shop.add_worker(self.admin)
        client_same_id = Client("Anna", date(1990, 1, 1), "A001")
        with self.assertRaises(DuplicateIDError):
            self.shop.add_client(client_same_id)

    def test_get_client(self):
        self.shop.add_client(self.client)
        result = self.shop.get_client("C001")
        self.assertEqual(result, self.client)

    def test_get_client_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.get_client("C999")

    def test_remove_client(self):
        self.shop.add_client(self.client)
        self.shop.remove_client("C001")
        self.assertNotIn(self.client, self.shop.get_all_clients())

    def test_remove_client_with_active_rental_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental("1234ABC", "C001", self.start, self.end, 500, "basic")
        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.remove_client("C001")

    def test_remove_client_with_finished_rental_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.past_start, self.past_end, 500, "basic"
        )
        self.shop.remove_client("C001")
        self.assertNotIn(self.client, self.shop.get_all_clients())

    def test_remove_client_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.remove_client("C999")

    def test_update_client_name(self):
        self.shop.add_client(self.client)
        self.shop.update_client_name("C001", "Maria")
        self.assertEqual(self.client.name, "Maria")

    def test_get_all_clients_returns_copy(self):
        self.shop.add_client(self.client)
        clients = self.shop.get_all_clients()
        clients.clear()
        self.assertEqual(len(self.shop.get_all_clients()), 1)

    # ── Workers ───────────────────────────────────────────────────────────────

    def test_add_worker(self):
        self.shop.add_worker(self.admin)
        self.assertIn(self.admin, self.shop.get_all_workers())

    def test_add_duplicate_worker_raises_error(self):
        self.shop.add_worker(self.admin)
        with self.assertRaises(DuplicateIDError):
            self.shop.add_worker(self.admin)

    def test_add_worker_same_id_as_client_raises_error(self):
        self.shop.add_client(self.client)
        worker_same_id = Admin("Test", date(1980, 1, 1), "C001", "mechanic")
        with self.assertRaises(DuplicateIDError):
            self.shop.add_worker(worker_same_id)

    def test_get_worker(self):
        self.shop.add_worker(self.admin)
        result = self.shop.get_worker("A001")
        self.assertEqual(result, self.admin)

    def test_get_worker_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.get_worker("A999")

    def test_remove_worker(self):
        self.shop.add_worker(self.admin)
        self.shop.remove_worker("A001")
        self.assertNotIn(self.admin, self.shop.get_all_workers())

    def test_remove_worker_not_found_raises_error(self):
        with self.assertRaises(UserNotFoundError):
            self.shop.remove_worker("A999")

    def test_update_worker_role(self):
        self.shop.add_worker(self.admin)
        self.shop.update_worker_role("A001", "administrator")
        self.assertEqual(self.admin.role, "administrator")

    def test_get_all_workers_returns_copy(self):
        self.shop.add_worker(self.admin)
        workers = self.shop.get_all_workers()
        workers.clear()
        self.assertEqual(len(self.shop.get_all_workers()), 1)

    # ── Assign Vehicle to Client ──────────────────────────────────────────────

    def test_assign_vehicle_to_client(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.assign_vehicle_to_client("1234ABC", "C001")
        self.assertIn(self.car, self.client.vehicles)

    def test_remove_vehicle_from_client(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.assign_vehicle_to_client("1234ABC", "C001")
        self.shop.remove_vehicle_from_client("1234ABC", "C001")
        self.assertNotIn(self.car, self.client.vehicles)

    def test_assign_vehicle_not_found_raises_error(self):
        self.shop.add_client(self.client)
        with self.assertRaises(VehicleNotFoundError):
            self.shop.assign_vehicle_to_client("9999ZZZ", "C001")

    def test_assign_client_not_found_raises_error(self):
        self.shop.add_vehicle(self.car)
        with self.assertRaises(UserNotFoundError):
            self.shop.assign_vehicle_to_client("1234ABC", "C999")

    # ── Rentals ───────────────────────────────────────────────────────────────

    def test_create_rental(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        rental = self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.assertIn(rental, self.shop.get_all_rentals())

    def test_create_rental_vehicle_not_found_raises_error(self):
        self.shop.add_client(self.client)
        with self.assertRaises(VehicleNotFoundError):
            self.shop.create_rental(
                "9999ZZZ", "C001", self.start, self.end, 500, "basic"
            )

    def test_create_rental_client_not_found_raises_error(self):
        self.shop.add_vehicle(self.car)
        with self.assertRaises(UserNotFoundError):
            self.shop.create_rental(
                "1234ABC", "C999", self.start, self.end, 500, "basic"
            )

    def test_create_overlapping_rental_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.create_rental(
                "1234ABC", "C002", self.start, self.end, 500, "basic"
            )

    def test_create_non_overlapping_rentals_ok(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental(
            "1234ABC", "C001", self.past_start, self.past_end, 500, "basic"
        )
        self.shop.create_rental(
            "1234ABC", "C002", self.future_start, self.future_end, 500, "basic"
        )
        self.assertEqual(len(self.shop.get_all_rentals()), 2)

    def test_different_vehicles_can_be_rented_simultaneously(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.create_rental(
            "5678DEF", "C001", self.start, self.end, 500, "basic"
        )
        self.assertEqual(len(self.shop.get_all_rentals()), 2)

    def test_get_rental(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        rental = self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        found = self.shop.get_rental("1234ABC", "C001", self.start)
        self.assertEqual(rental, found)

    def test_get_rental_not_found_raises_error(self):
        with self.assertRaises(RentalNotFoundError):
            self.shop.get_rental("1234ABC", "C001", self.today)

    def test_get_active_rentals(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.create_rental(
            "5678DEF", "C001", self.past_start, self.past_end, 500, "basic"
        )
        active = self.shop.get_active_rentals()
        self.assertEqual(len(active), 1)

    def test_get_finished_rentals(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.create_rental(
            "5678DEF", "C001", self.past_start, self.past_end, 500, "basic"
        )
        finished = self.shop.get_finished_rentals()
        self.assertEqual(len(finished), 1)

    def test_modify_rental_end_date(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        new_end = self.today + relativedelta(days=15)
        self.shop.modify_rental("1234ABC", "C001", self.start, new_end_date=new_end)
        rental = self.shop.get_rental("1234ABC", "C001", self.start)
        self.assertEqual(rental.end_date, new_end)

    def test_modify_rental_overlap_raises_error(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.add_client(self.client2)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.create_rental(
            "1234ABC", "C002",
            self.today + relativedelta(days=20),
            self.today + relativedelta(days=30),
            500, "basic"
        )
        with self.assertRaises(VehicleAlreadyRentedError):
            self.shop.modify_rental(
                "1234ABC", "C001", self.start,
                new_end_date=self.today + relativedelta(days=25)
            )

    def test_add_kms_to_rental(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.add_kms_to_rental("1234ABC", "C001", self.start, 100)
        rental = self.shop.get_rental("1234ABC", "C001", self.start)
        self.assertEqual(rental.kms_done, 100)

    def test_add_kms_updates_vehicle_mileage(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        self.shop.add_kms_to_rental("1234ABC", "C001", self.start, 100)
        self.assertEqual(self.car.mileage, 50100)

    def test_get_all_rentals_returns_copy(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_client(self.client)
        self.shop.create_rental(
            "1234ABC", "C001", self.start, self.end, 500, "basic"
        )
        rentals = self.shop.get_all_rentals()
        rentals.clear()
        self.assertEqual(len(self.shop.get_all_rentals()), 1)

    # ── str ───────────────────────────────────────────────────────────────────

    def test_str_shows_correct_counts(self):
        self.shop.add_vehicle(self.car)
        self.shop.add_vehicle(self.car2)
        self.shop.add_client(self.client)
        self.shop.add_worker(self.admin)
        result = str(self.shop)
        self.assertIn("2 vehicles", result)
        self.assertIn("1 clients", result)
        self.assertIn("1 workers", result)

    def test_str_shows_zero_when_empty(self):
        result = str(self.shop)
        self.assertIn("0 vehicles", result)
        self.assertIn("0 clients", result)


if __name__ == "__main__":
    unittest.main()
