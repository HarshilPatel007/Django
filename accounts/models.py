from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.


# Custom User Model
class CustomUsersManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not date_of_birth:
            raise ValueError("User must have a date of birth")

        custom_user = self.model(

            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
        )

        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(self, email, username, first_name, last_name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        super_user = self.model(

            email,
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth
        )

        super_user.is_admin = True
        # super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True, null=False, blank=False)
    username = models.CharField(verbose_name="username", max_length=50, unique=True, null=False, blank=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True, null=False, blank=False)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(verbose_name="first name", max_length=50, null=False, blank=False)
    last_name = models.CharField(verbose_name="last name", max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(verbose_name="date of birth", null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']

    objects = CustomUsersManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Customer(models.Model):
    user = models.OneToOneField(CustomUserModel, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    mobile_number = models.CharField(max_length=15, null=False)
    profile_pic = models.ImageField(default="default-profile.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    # address = models.TextField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.user.get_full_name()


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=100, null=False)
    price = models.FloatField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False, choices=CATEGORY)
    description = models.TextField(max_length=500, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, null=False, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        template = '{0.customer} {0.product} {0.status}'
        return template.format(self)


