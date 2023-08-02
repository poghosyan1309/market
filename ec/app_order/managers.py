from datetime import datetime
from django.db import models

class ActiveCouponManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, valid_from_lt=datetime.now(), valid_to_gt=datetime.now())
