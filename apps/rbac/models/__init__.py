# keep User model at the top
from .user import User
# ===================
from .branch import Branch
from .department import Department
from .user_password import UserPassword
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
