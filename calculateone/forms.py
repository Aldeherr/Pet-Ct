from cProfile import label
from pickletools import decimalnl_long
from pydoc import Helper
from socket import fromshare
from tkinter import Widget
from django import forms


class barrier(forms.Form):

    factor_choices = (('1','1'),
        (0.5,'1/2'),
        (0.2,'1/5'),
        (0.125,'1/8'),
        (0.05,'1/20'),
        (0.025,'1/40'))
    dose_choices = ((20,'20 µSv x semana'),
        (100,'100 µSv x semana'))
    
    dose = forms.ChoiceField(choices=dose_choices, 
        label='Dosis Permisible',
        widget=forms.Select(attrs={'class':'form-select'})
        )
    factor = forms.ChoiceField(choices=factor_choices, 
        label='Factor de Ocupacion',
        widget=forms.Select(attrs={'class':'form-select'}))

    distance = forms.FloatField(label='Distance',
        widget=forms.NumberInput(
            attrs={'step':'0.01', 'class':'form-control'})
        )

class pet_form(forms.Form):

    ao = forms.FloatField(label='Actividad Inicial',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))
    hr_patients = forms.FloatField( label='N. Pacientes',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))
    study_time = forms.FloatField( label='Tiempo de Estudio',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))


class cet_form(forms.Form):
    ct_prct = forms.FloatField( label='% Contraste',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))
    ct_num_body = forms.FloatField( label='# Pacientes Head',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))
    ct_num_head = forms.FloatField( label='# Pacientes Body',
        widget=forms.NumberInput(attrs={'step':'0.02', 'class':'form-control'}))

class details(forms.Form):

    metric = (
        (1000,'M'),
        (1,'cm')
    )

    barrier_id = forms.CharField(label='Nombre de la barrera', 
                    widget=forms.TextInput(attrs={'class':'form-control'}),
                    help_text="<span class=\"tooltip\">?<span class=\"tooltiptext\">Introducir el nombre de la pared a calcular</span></span>" ,)
    # unidad = forms.ChoiceField(choices=metric,
    #     label='Unidad de Distancia',
    #     widget=forms.Select(attrs={'class':'form-select'})
    # )

