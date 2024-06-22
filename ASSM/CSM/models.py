from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.safestring import mark_safe

# Custom Author Manager 
class AuthorManager(BaseUserManager):
    def create_user(self, email, First_name, Last_name, phone_no, pincode, password=None, password2=None):
        """
        Creates and saves a User with the given email, First_name
        Last_name, Phone_no, pincode and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            First_name = First_name,
            Last_name = Last_name,
            phone_no = phone_no,
            pincode = pincode,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, First_name, Last_name, phone_no, pincode, password=None):
        """
        Creates and saves a User with the given email, First_name
        Last_name, Phone_no, pincode and password.
        """
        user = self.create_user(
            email,
            password=password,
            First_name= First_name,
            Last_name= Last_name,
            phone_no= phone_no,
            pincode = pincode,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

# Author Model
class Author(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    First_name= models.CharField(
        max_length=50,
    )
    Last_name= models.CharField(max_length=25)
    phone_no = PhoneNumberField(
        null=True, 
    )
    pincode = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuthorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["First_name", "Last_name", "phone_no", "pincode"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Author_content(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pdf')

    def image_tag(self): #new
        return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')

    def __str__(self):
        return self.user.First_name