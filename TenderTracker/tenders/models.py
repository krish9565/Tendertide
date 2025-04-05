from django.utils import timezone
from django.conf import settings
from djongo import models #as djongo_models  # Import Djongo models

# class Tender(djongo_models.Model):  # Use djongo_models.Model instead of models.Model
#     TENDER_TYPES = [
#         ('government', 'Government'),
#         ('private', 'Private'),
#         ('international', 'International'),
#     ]
    
#     CATEGORIES = [
#         ('construction', 'Construction'),
#         ('it', 'Information Technology'),
#         ('healthcare', 'Healthcare'),
#         ('education', 'Education'),
#         ('infrastructure', 'Infrastructure'),
#         ('energy', 'Energy'),
#         ('transportation', 'Transportation'),
#         ('telecommunications', 'Telecommunications'),
#         ('agriculture', 'Agriculture'),
#         ('defense', 'Defense'),
#     ]

#     _id = djongo_models.ObjectIdField()  # Explicitly define the _id field for MongoDB
#     title = djongo_models.CharField(max_length=200)  # Using Djongo's CharField
#     description = djongo_models.TextField()
#     type = djongo_models.CharField(max_length=50, choices=TENDER_TYPES)
#     category = djongo_models.CharField(max_length=50, choices=CATEGORIES)
#     deadline = djongo_models.DateTimeField()
#     value = djongo_models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     location = djongo_models.CharField(max_length=100)
#     requirements = djongo_models.TextField(blank=True)
#     scope = djongo_models.TextField(blank=True)
#     status = djongo_models.CharField(max_length=20, default='active')
#     author = djongo_models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=djongo_models.SET_NULL, null=True)
#     created_at = djongo_models.DateTimeField(default=timezone.now)
#     updated_at = djongo_models.DateTimeField(auto_now=True)
#     favorited_by = djongo_models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='favorite_tenders',
#         through='TenderFavorite'
#     )

#     class Meta:
#         db_table = 'users'  # Specify MongoDB collection name
#         ordering = ['-created_at']
#         indexes = [
#             djongo_models.Index(fields=['type']),
#             djongo_models.Index(fields=['category']),
#             djongo_models.Index(fields=['status']),
#             djongo_models.Index(fields=['deadline']),
#             djongo_models.Index(fields=['location']),
#         ]

#     def __str__(self):
#         return self.title




class ContactMessage(models.Model):
    _id = models.ObjectIdField()  # MongoDB ObjectId
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

    class Meta:
        db_table = "contact_messages"  # MongoDB Collection Name


class Tender(models.Model):
    _id = models.ObjectIdField()
    tender_number = models.CharField(max_length=50)
    publication_date = models.CharField(max_length=50)
    deadline = models.CharField(max_length=50, blank=True, null=True)
    tender_title = models.CharField(max_length=200)
    tender_link = models.URLField()
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return self.tender_title
    class Meta:
        db_table = 'users'
    
    
class TenderFavorite(models.Model):  # Use djongo_models.Model for consistency
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'tender')
