from django import forms

from coop.base.models import Cooperative, Unit


class CooperativeForm(forms.ModelForm):
    cooperative_name = forms.CharField(label='Cooperative Name')

    class Meta:
        model = Cooperative
        fields = ('cooperative_name',)

    def clean_cooperative_name(self):
        cooperative_name = self.cleaned_data.get("cooperative_name")
        invalid = cooperative_name.strip() == ""
        if invalid:
            raise forms.ValidationError("Cooperative Name must be filled")
        return cooperative_name

    def save(self, commit=True):
        cooperative = super(CooperativeForm, self).save(commit=False)
        cooperative.set_cooperative_name(self.cleaned_data['cooperative_name'])
        if commit:
            cooperative.save()
        return cooperative


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ('cooperative_id', 'unit_number')
        labels = {
            'cooperative_id': 'Cooperative name',
        }
