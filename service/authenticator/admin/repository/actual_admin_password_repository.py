from typing import Optional

from peewee import DoesNotExist

from hash.hashed_str import HashedStr
from service.authenticator.admin.model.admin_password import AdminPassword
from service.authenticator.admin.repository.admin_password_entity import AdminPasswordEntity
from service.authenticator.admin.repository.admin_password_repository import AdminPasswordRepository


class ActualAdminPasswordRepository(AdminPasswordRepository):
    AdminPasswordEntity.create_table(safe=True)

    def get_password(self) -> Optional[AdminPassword]:
        try:
            password_entity: AdminPasswordEntity = AdminPasswordEntity.get()
            return AdminPassword(
                hash=HashedStr(
                    value=password_entity.hash,
                    salt=password_entity.salt,
                ),
                version=password_entity.version,
            )
        except DoesNotExist:
            return None

    def update_password(self, new_password: AdminPassword):
        try:
            password_entity: AdminPasswordEntity = AdminPasswordEntity.get()
            password_entity.hash = new_password.hash.value
            password_entity.salt = new_password.hash.salt
            password_entity.version = new_password.version
            password_entity.save()
        except DoesNotExist:
            AdminPasswordEntity.create(
                hash=new_password.hash.value,
                salt=new_password.hash.salt,
                version=new_password.version,
            )
