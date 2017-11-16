from django import forms
from history.models import HistEntry


class TransferForm(forms.Form):
    order_id = forms.ModelChoiceField(
        required=True,
        queryset=HistEntry.objects.none()
    )
    value = forms.DecimalField(
        required=True,
        max_digits=10
    )
    transfer_date = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields["order_id"].queryset = HistEntry.objects.filter(
            user=self.request.user_id,
            status='WAITING',
            pay_method='CASH',
        )
