import django_tables2 as tables
from .models import HistEntry, HistData
from Catalog.models import Product
from django_tables2.utils import A
import uuid


class HistEntryTable(tables.Table):
    order_id = tables.LinkColumn(
        'details',
        args=[A('pk')],
        text=lambda record: str(record.order_id)[:8]
        )

    class Meta:
        model = HistEntry
        attrs = {'class': 'table table-responsive'}
        exclude = ('user')
        sequence = ('order_time', '...',)


class HistDataTable(tables.Table):
    product_id = tables.LinkColumn(
        'Catalog:detail',
        args=[A('product_id')],
        text=lambda record: str(
            Product.objects.get(product_id=record.product_id).name
            # record.product_id
        )
    )

    class Meta:
        model = HistData
        attrs = {'class': 'table table-responsive'}
        exclude = ('order_id', 'entry_id')
