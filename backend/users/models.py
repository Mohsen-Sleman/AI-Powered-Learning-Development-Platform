from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Level(models.TextChoices):
        BEGINNER = 'BEG', _('Beginner')
        INTERMEDIATE = 'INT', _('Intermediate')
        ADVANCED = 'ADV', _('Advanced')

class RoleChoices(models.TextChoices) :
        STUDENT = "STU" , _("Student")
        INSTRUCTOR = "INS", _("Instructor")

class UserManager(BaseUserManager) :
    def create_user(self,email,full_name,password=None,**extra_fields) :
        """
        Creates and saves a regular User with the given email, full_name, and password.
        Raises ValueError if email is missing or already registered.
        """
        if not email : 
            raise ValueError('A valid email address must be provided.')
        
        if self.model.objects.filter(email=email).exists() : 
            raise ValueError('This email address is already registered.')

        
        user = self.model(email=email,full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,email,full_name,password=None,**extra_fields) :

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,full_name,password,**extra_fields)



class User(AbstractBaseUser,PermissionsMixin) :

    email = models.EmailField(unique=True, max_length=200)
    full_name = models.CharField(max_length=50)
    role = models.CharField(max_length=3,choices=RoleChoices.choices,default=RoleChoices.STUDENT)
    skill_level = models.CharField(max_length=3,choices=Level.choices,default=Level.BEGINNER)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','role','profile_picture']

