from django import forms
from django.core.validators import MinValueValidator
from calculator.calculator import PROJECT_TYPES_BASIC_COCOMO1, PROJECT_TYPES_INTERMEDIATE_COCOMO1, CDS, ESTIMATES, SFS


class BasicCOCOMO1Form(forms.Form):
    project_type = forms.ChoiceField(
        choices=(
            (project_type, project_type)
            for project_type in PROJECT_TYPES_BASIC_COCOMO1.keys()
        ),
        label='Тип проекта'
    )
    size = forms.FloatField(
        label='Объём ПО в тыс. строках кода',
        validators=[MinValueValidator(float(0.001))]
    )

    def clean(self):
        super(BasicCOCOMO1Form, self).clean()

        if not self.cleaned_data.get('size'):
            raise forms.ValidationError(message='Проверьте заполненные данные')


class IntermediateCOCOMO1Form(forms.Form):
    project_type = forms.ChoiceField(
        choices=(
            (project_type, project_type)
            for project_type in PROJECT_TYPES_INTERMEDIATE_COCOMO1.keys()
        ),
        label='Тип проекта'
    )
    size = forms.FloatField(
        label='Объём ПО в тыс. строках кода',
        validators=[MinValueValidator(float(0.001))]
    )

    def __init__(self, *args, **kwargs):
        super(IntermediateCOCOMO1Form, self).__init__(*args, **kwargs)

        for number, data in enumerate(CDS.items(), start=1):
            cd_name, levels = data
            self.fields[f'param_{number}'] = forms.ChoiceField(
                choices=(
                    (param_name, param_name)
                    for param_name in levels.keys()
                ),
                label=f'{number}. {cd_name}',
                initial='средний',
            )

    def clean(self):
        super(IntermediateCOCOMO1Form, self).clean()

        if not self.cleaned_data.get('size'):
            raise forms.ValidationError(message='Проверьте заполненные данные')


class COCOMO2Form(forms.Form):
    size = forms.FloatField(
        label='Объём ПО в тыс. строках кода',
        validators=[MinValueValidator(float(0.001))]
    )

    def __init__(self, *args, **kwargs):
        estimate = kwargs.pop('estimate')
        super(COCOMO2Form, self).__init__(*args, **kwargs)

        start = 1
        for number, data in enumerate(ESTIMATES[estimate].items(), start=start):
            em_name, levels = data
            self.fields[f'em_{number}'] = forms.ChoiceField(
                choices=(
                    (param_name, param_name)
                    for param_name in levels.keys()
                ),
                label=f'{number}. {em_name}',
                initial='средний',
            )
            start += 1

        for number, data in enumerate(SFS.items(), start=start):
            sf_name, levels = data
            self.fields[f'sf_{number}'] = forms.ChoiceField(
                choices=(
                    (param_name, param_name)
                    for param_name in levels.keys()
                ),
                label=f'{number}. {sf_name}',
                initial='средний',
            )


class ResultForm(forms.Form):
    pm = forms.CharField(label='Трудоемкость(PM), чел.× мес')
    pm.widget.attrs['readonly'] = True
    tm = forms.CharField(label='Время разработки(TM), мес')
    tm.widget.attrs['readonly'] = True

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
