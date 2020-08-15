from django import forms


class BinaryWidget(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        value = super(BinaryWidget, self).value_from_datadict(data, files, name)
        if name == 'shifts':
            value = bytearray.fromhex(''.join([hex(x)[2:] for x in value]))
        return value


class ImportForm(forms.Form):
    file = forms.FileField()