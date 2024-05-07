from abc import ABC, abstractmethod
from typing import Optional

from service.authenticator.admin.model.admin_password import AdminPassword


class AdminPasswordRepository(ABC):
    @abstractmethod
    def get_password(self) -> Optional[AdminPassword]:
        pass

    @abstractmethod
    def update_password(self, new_password: AdminPassword):
        pass
