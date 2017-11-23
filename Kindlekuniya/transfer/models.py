from django.db import models
from history.models import HistEntry
from user.models import User
import uuid


class TransferEntry(models.Model):
    entry_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    order_id = models.ForeignKey(HistEntry, on_delete=models.CASCADE,)
    value = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        verbose_name="Total Transfer"
    )
    transfer_date = models.DateTimeField(
        verbose_name="Transfer Date"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )

    def __str__(self):
        return str(self.order_id)[:8]
