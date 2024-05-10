from django.contrib.auth.models import  UserManager


class ProfileManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        # Remove the 'username' field from extra_fields
        extra_fields.pop('username', None)
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Add a default username if it doesn't exist in extra_fields
        extra_fields.setdefault('username', email)

        return self.create_user(email, password, **extra_fields)