from django import forms


class BinaryWidget(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        value = super(BinaryWidget, self).value_from_datadict(data, files, name)
        arr = bytearray.fromhex('00 00 00 00')
        for s in value:
            arr[s] = 1
        return arr
    
    def decompress(self, value):
        return list(map(lambda x: x[0], filter(lambda y: y[1], enumerate(value))))


class MultiSelectors(forms.MultiWidget):
    def __init__(self, attrs=None):
        STATES = [(0, 'нет'), (1, 'д'), (2, 'н')]
        widgets = [
            forms.Select(choices=STATES),
            forms.Select(choices=STATES),
            forms.Select(choices=STATES),
            forms.Select(choices=STATES)
        ]
        super().__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        value = super(MultiSelectors, self).value_from_datadict(data, files, name)
        return bytearray.fromhex(''.join(['0' + str(x) for x in value]))
    
    def decompress(self, value):
        if type(value) == bytearray:
            return [int(x) for x in value]
        return [None] * 4


class ImportForm(forms.Form):
    file = forms.FileField()