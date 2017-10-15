import django_tables2 as tables
from .models import HistEntry, HistData
from django_tables2.utils import A


class HistEntryTable(tables.Table):
    orderId = tables.LinkColumn(
        'details',
        args=[A('pk')],
        text=lambda record: str(record.orderId)[:8]
    )

    class Meta:
        model = HistEntry
        attrs = {'class': 'paleblue'}
        exclude = ('orderOwner', 'id')
        sequence = ('orderTime', '...',)


class HistDataTable(tables.Table):
    """
    orderName = tables.LinkColumn('PRODUCT_DETAIL', args = [A('pk')], text = lambda record: record.PRODUCT_NAME[:64])
    quantity
    total price
    tax
    """

    class Meta:
        model = HistData
        attrs = {'class': 'paleblue'}
        exclude = ('orderId', 'id')
