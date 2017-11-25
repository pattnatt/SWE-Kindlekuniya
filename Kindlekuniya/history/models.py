from django.db import models
from Catalog.models import Product
from user.models import User, Address
import uuid


class HistEntry(models.Model):
    order_id = models.AutoField(verbose_name='Order ID', primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    order_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Order Time'
    )
    WAITING = 'WAITING'
    PROCESS = 'PROCESS'
    TRANSIT = 'TRANSIT'
    RECEIVE = 'RECEIVE'
    SHIPPING_STATUSES = (
        (PROCESS, 'Processing'),
        (TRANSIT, 'In Transit'),
        (RECEIVE, 'Received'),
        (WAITING, 'Waiting for Payment'),
        )
    status = models.CharField(
        max_length=7,
        choices=SHIPPING_STATUSES,
        default=WAITING
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    tracking_no = models.CharField(
        max_length=16,
        blank=True,
        default='',
        verbose_name='Tracking No.',
        )
    CREDIT = 'CREDIT'
    CASH = 'CASH'
    PAYMENT_METHODS = (
        (CREDIT, 'Credit Card'),
        (CASH, 'Cash Transfer'),
        )
    pay_method = models.CharField(
        max_length=7,
        choices=PAYMENT_METHODS,
        default=CASH,
        verbose_name="Payment Method"
    )
    shipping_price = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.order_id)[:8] + ' - ' + str(self.order_time)[:16]


class HistData(models.Model):
    entry_id = models.AutoField(verbose_name='Entry ID', primary_key=True)
    order_id = models.ForeignKey(HistEntry, on_delete=models.CASCADE,)
    product_id = models.CharField(
        max_length=36,
        default=None,
        verbose_name='Product'
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    sum_price = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="Total Price"
    )
    tax = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        verbose_name="After Tax"
    )

    def __str__(self):
        return str(self.order_id)[:8] + '-' + str(self.product_id)
