from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.base_user import AbstractBaseUser
from utils.common import USER_ROLES

class CustomAdminAuthForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        if user.role != USER_ROLES.ADMIN.value:
            raise self.get_invalid_login_error()
    
    