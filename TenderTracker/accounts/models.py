from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    ACCOUNT_TYPES = [
        ('user', 'Individual User'),
        ('company', 'Company'),
        ('admin', 'Administrator'),
    ]

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='user'
    )
    company_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Add this field
    favorite_tenders = models.ManyToManyField('tenders.Tender', blank=True, related_name='favorited_by')

    class Meta:
        indexes = [
            models.Index(fields=['account_type']),
            models.Index(fields=['is_active']),
        ]

    def clean(self):
        """ Custom validation to ensure company name is provided for company account type. """
        if self.account_type == 'company' and not self.company_name:
            raise ValidationError({'company_name': 'Company name is required for company account type.'})

    def save(self, *args, **kwargs):
        # Run custom clean method for validation
        self.clean()
        super().save(*args, **kwargs)

    def is_company(self):
        return self.account_type == 'company'

    def is_admin_user(self):
        return self.account_type == 'admin'

    def __str__(self):
        return self.username
