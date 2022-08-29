from http.client import HTTPResponse
from multiprocessing import Barrier, context
from tkinter import EXCEPTION
from unittest import result
from django.shortcuts import render
from .forms import barrier, pet_form, cet_form, details
import math as mth
# Create your views here.


def calculator(request):
    barrier_form = barrier
    pet = pet_form
    ct = cet_form
    detail = details

    context = {
        'barrier_form': barrier_form,
        'pet_form': pet,
        'ct_form': ct,
        'detail': detail
    }
    return render(request, 'calculateone/main.html', context)


def compute(request):

    if request.method == 'POST':
        form_barrier = barrier(request.POST)
        form_detail = details(request.POST)
        form_pet = pet_form(request.POST)
        form_ct = cet_form(request.POST)

        context = {}

        if form_barrier.is_valid() and form_detail.is_valid():
            # Variables Generales
            factor_ocup = form_barrier.cleaned_data['factor']
            dosis = form_barrier.cleaned_data['dose']
            distance = form_barrier.cleaned_data['distance']
            detail = form_detail.clean()
            NameBarrier = detail['barrier_id']


            if form_ct.is_valid() and NameBarrier:

                prct = form_ct.cleaned_data['ct_prct']
                patients_head = form_ct.cleaned_data['ct_num_body']
                patients_body = form_ct.cleaned_data['ct_num_head']

                ksecbody, ksechead = ct_params(
                    prct, patients_head, patients_body, dosis, factor_ocup, distance)

                context_ct = {
                    'barrier_id': NameBarrier,
                    'dose': dosis,
                    'factor': factor_ocup,
                    'ct_concrete': round(ksecbody, 3),
                    'ct_lead': round(ksechead, 3),
                }

                context.update(context_ct)
            else:
                context_ct = {
                    'barrier_id': NameBarrier,
                    'dose': dosis,
                    'factor': factor_ocup,
                    'ct_concrete': '0',
                    'ct_lead': '0',
                }
            context.update(context_ct)

            if form_pet.is_valid():

                # VARIABLES PET
                ao = form_pet.cleaned_data['ao']
                n = form_pet.cleaned_data['hr_patients']
                ti = form_pet.cleaned_data['study_time']

                rpa = 0.092
                rti = 0.91  # Se deja seleccionable o solo este valor estatico?
                fu = 0.68
                rr = 0.83

                # Calculos
                total_dose_partial = (rpa*rti*fu*rr)
                total_dose = (((ao)*(ti)*(n)) * total_dose_partial)/((distance))**2
                transmision = (float(dosis)) / \
                    (float(total_dose) * float(factor_ocup))

                archer_pet = {'a': {'lead': 1.5430, 'concrete': 0.1539, 'iron': 0.5704},
                            'b': {'lead': -0.4408, 'concrete': -0.1161, 'iron': -0.3063},
                            'y': {'lead': 2.1360, 'concrete': 2.0752, 'iron': 0.6326}}

                # base_log_concrete = (((total_dose)**-archer_pet['y']['concrete']+(archer_pet['']))/(1+()))
                pet_concrete = archer_equa(transmision, archer_pet['y']['concrete'],
                                        archer_pet['b']['concrete'], archer_pet['a']['concrete'])
                pet_lead = archer_equa(transmision, archer_pet['y']['lead'],
                                    archer_pet['b']['lead'], archer_pet['a']['lead'])

                context_pet = {
                    'barrier_id': NameBarrier,
                    'dose': dosis,
                    'factor': factor_ocup,
                    'pet_concrete': round(pet_concrete, 3),
                    'pet_lead': round(pet_lead, 3),
                }

                context.update(context_pet)
            else:
                context_pet = {
                'barrier_id': NameBarrier,
                'dose': dosis,
                'factor': factor_ocup,
                'pet_concrete': '0',
                'pet_lead': '0',
                }
                context.update(context_pet)

        else:
            context_null = {
                'barrier_id': "#",
                'dose': '#',
                'factor': '#',
                'pet_concrete': '0',
                'pet_lead': '0',
                'ct_concrete': '0',
                'ct_lead': '0',
            }
            context.update(context_null)

        return render(request, 'calculateone/partial.html', context)


def archer_equa(b1, gamma, beta, alpha):
    try:
        potencia = b1 ** (-gamma)
        ba = beta/alpha
        upper_log = (potencia + ba) / (1+ba)
        log_part = mth.log(upper_log)
        total_espesor = (1/(alpha * gamma)) * log_part
    except:
        total_espesor = 0
    return total_espesor


def ct_params(prct, patients_head, patients_body, dosis, factor_ocup, distance):

    # FIELDS DEFINED
    khead = 0.00009
    kbody = 0.0003
    DLPhead = 1200  # MGY.cm
    DLPbody = 550  # MGY.cm

    archer_ct = {'a': {'lead': 2.009, 'concrete': 0.0336},
                 'b': {'lead': 3.99, 'concrete': 0.0122},
                 'y': {'lead': 0.342, 'concrete': 0.519}
                 }

    # KERMA SECUNDARIO
    try:

        KsecBody = (1.2 * kbody * DLPbody * prct) * 1000
        KsecHead = (khead * DLPhead * prct) * 1000
        total_dose = ((patients_head*KsecHead) +
                      (patients_body*KsecBody))*((1/distance)**2)
        transmision = ((float(dosis))/(float(total_dose) * float(factor_ocup)))

        ct_concrete = archer_equa(transmision, archer_ct['y']['concrete'],
                                  archer_ct['b']['concrete'], archer_ct['a']['concrete'])

        ct_lead = archer_equa(transmision, archer_ct['y']['lead'],
                              archer_ct['b']['lead'], archer_ct['a']['lead'])
    except:
        ct_concrete = 0
        ct_lead = 0

    return ct_concrete/10, ct_lead/10
