from django.db import models
from .utils import encode_base62

class URLMapping(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=15, unique=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Save first to get a Primary Key (ID)
        if not self.pk:
            super().save(*args, **kwargs)
        
        # 2. Generate short_code from ID if it doesn't exist
        if not self.short_code:
            self.short_code = encode_base62(self.pk)
            # 3. Update only the short_code field
            kwargs['force_insert'] = False
            super().save(update_fields=['short_code'])
        else:
            super().save(*args, **kwargs)