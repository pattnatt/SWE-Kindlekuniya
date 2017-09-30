from django.db import models
from Catalog.models import Product
import uuid


class HistEntry(models.Model):
    orderId = models.UUIDField(
        verbose_name='Order ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    # userID = models.ForeignKey(User, on_delete=models.CASCADE,)
    orderOwner = models.CharField(max_length=64)
    orderTime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Order Time'
    )
    PROCESS = 'PROCESS'
    TRANSIT = 'TRANSIT'
    RECEIVE = 'RECEIVE'
    SHIPPING_STATUSES = (
        (PROCESS, 'Processing'),
        (TRANSIT, 'In Transit'),
        (RECEIVE, 'Received'),
        )
    status = models.CharField(
        max_length=7,
        choices=SHIPPING_STATUSES,
        default=PROCESS
    )
    # shippingMethod = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    trackingNo = models.CharField(
        max_length=16,
        blank=True,
        default='',
        verbose_name='Tracking No.',
        )
    CREDIT = 'CREDIT'
    CASH = 'CASH'
    PAYMENT_METHODS = (
        (CREDIT, 'Credit Card'),
        # (CASH, 'Cash Transfer'),
        )
    payMethod = models.CharField(
        max_length=7,
        choices=PAYMENT_METHODS,
        default=CREDIT,
        verbose_name="Payment Method"
    )

    def __str__(self):
        return str(self.orderId)[:8] + '-' + str(self.orderTime)


class HistData(models.Model):
    orderId = models.ForeignKey(HistEntry, on_delete=models.CASCADE,)
    productID = models.ForeignKey(Product, on_delete = models.CASCADE, null = True, default = None)
    # orderName = models.CharField(max_length=300, verbose_name="Product Name")
    quantity = models.PositiveSmallIntegerField(default=1)
    sumPrice = models.DecimalField(
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
        return str(self.orderId)[:8] + '-' + str(self.productID)
