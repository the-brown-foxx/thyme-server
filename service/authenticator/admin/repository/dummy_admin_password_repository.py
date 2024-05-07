from typing import Optional

from service.authenticator.admin.model.admin_password import AdminPassword
from service.authenticator.admin.repository.admin_password_repository import AdminPasswordRepository


class DummyAdminPasswordRepository(AdminPasswordRepository):
    password: Optional[AdminPassword] = None

    def get_password(self) -> Optional[AdminPassword]:
        return self.password

    def update_password(self, new_password: AdminPassword):
        self.password = new_password
