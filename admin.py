from user import User
from exceptions import InvalidRoleError


class Admin(User):

    VALID_ROLES = (
        "mechanic",
        "rental manager",
        "administrator"
    )

    def __init__(self, name, date_of_birth, user_id, role):
        super().__init__(name, date_of_birth, user_id)

        if role.lower() not in self.VALID_ROLES:
            raise InvalidRoleError(
                f"Invalid role. Choose from {self.VALID_ROLES}"
            )

        self.__role = role.lower()

    @property
    def role(self):
        return self.__role

    def update_role(self, new_role):
        if new_role.lower() not in self.VALID_ROLES:
            raise InvalidRoleError(
                f"Invalid role. Choose from {self.VALID_ROLES}"
            )

        self.__role = new_role.lower()

    def get_info(self):
        return (
            f"Admin | {self.name} | ID: {self.user_id} "
            f"| Role: {self.role}"
        )

    def to_csv_row(self):
        row = super().to_csv_row()
        row["role"] = self.role
        return row