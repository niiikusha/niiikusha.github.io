from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View

from calculator.forms import BasicCOCOMO1Form, IntermediateCOCOMO1Form, ResultForm, COCOMO2Form
from calculator.calculator import BasicCOCOMO1, IntermediateCOCOMO1, COCOMO2


class CalculatorView(View):
    def get(self, request, **kwargs):
        session = request.session
        if kwargs.get('cocomo_version') == 1:
            form = BasicCOCOMO1Form(initial=session.get('cocomo_1')) if session.get('cocomo_1') else BasicCOCOMO1Form()
            result_form = ResultForm(initial=session.get('cocomo_1_result')) if session.get('cocomo_1_result') else None
            calculator_name = 'COCOMO (базовый уровень)'

        elif kwargs.get('cocomo_version') == 2:
            form = IntermediateCOCOMO1Form(initial=session.get('cocomo_2')) if session.get(
                'cocomo_2') else IntermediateCOCOMO1Form()
            result_form = ResultForm(initial=session.get('cocomo_2_result')) if session.get('cocomo_2_result') else None
            calculator_name = 'COCOMO (промежуточный уровень)'

        elif kwargs.get('cocomo_version') == 3:
            form = COCOMO2Form(initial=session.get('cocomo_3'), estimate='предварительная') if session.get(
                'cocomo_3') else COCOMO2Form(estimate='предварительная')
            result_form = ResultForm(initial=session.get('cocomo_3_result')) if session.get('cocomo_3_result') else None
            calculator_name = 'COCOMO II (предварительная оценка)'

        elif kwargs.get('cocomo_version') == 4:
            form = COCOMO2Form(initial=session.get('cocomo_4'), estimate='детальная') if session.get(
                'cocomo_4') else COCOMO2Form(estimate='детальная')
            result_form = ResultForm(initial=session.get('cocomo_4_result')) if session.get('cocomo_4_result') else None
            calculator_name = 'COCOMO II (детальная оценка)'

        else:
            return HttpResponseRedirect(reverse('calculator:main'))

        context = {
            'form': form,
            'result_form': result_form,
            'calculator_name': calculator_name,
        }
        return render(request, 'calculator/calculator.html', context)

    def post(self, request, **kwargs):
        if kwargs.get('cocomo_version') == 1:
            calculator_name = 'COCOMO (базовый уровень)'
            form = BasicCOCOMO1Form(request.POST)

            if form.is_valid():
                result = BasicCOCOMO1(
                    project_type=form.cleaned_data.get('project_type'),
                    size=form.cleaned_data.get('size'),
                )
                result_form = ResultForm(initial={'pm': str(result.pm), 'tm': str(result.tm)})

                request.session['cocomo_1'] = request.POST
                request.session['cocomo_1_result'] = {'pm': str(result.pm), 'tm': str(result.tm)}

                context = {
                    'result_form': result_form,
                    'form': form,
                    'calculator_name': calculator_name,
                }
                return render(request, 'calculator/calculator.html', context)

            context = {
                'form': form,
                'calculator_name': calculator_name,
            }
            return render(request, 'calculator/calculator.html', context)

        elif kwargs.get('cocomo_version') == 2:
            calculator_name = 'COCOMO (промежуточный уровень)'
            form = IntermediateCOCOMO1Form(request.POST)

            if form.is_valid():
                result = IntermediateCOCOMO1(
                    project_type=form.cleaned_data.get('project_type'),
                    size=form.cleaned_data.get('size'),
                    cds=[
                        form.cleaned_data[param_name]
                        for param_name in form.cleaned_data.keys()
                        if 'param' in param_name
                    ]
                )
                result_form = ResultForm(initial={'pm': str(result.pm), 'tm': str(result.tm)})

                request.session['cocomo_2'] = request.POST
                request.session['cocomo_2_result'] = {'pm': str(result.pm), 'tm': str(result.tm)}

                context = {
                    'result_form': result_form,
                    'form': form,
                    'calculator_name': calculator_name,
                }
                return render(request, 'calculator/calculator.html', context)

            context = {
                'form': form,
                'calculator_name': calculator_name,
            }
            return render(request, 'calculator/calculator.html', context)

        elif kwargs.get('cocomo_version') == 3:
            calculator_name = 'COCOMO II (предварительная оценка)'
            form = COCOMO2Form(request.POST, estimate='предварительная')

            if form.is_valid():
                result = COCOMO2(
                    ems=[
                        form.cleaned_data[param_name]
                        for param_name in form.cleaned_data.keys()
                        if 'em' in param_name
                    ],
                    sfs=[
                        form.cleaned_data[param_name]
                        for param_name in form.cleaned_data.keys()
                        if 'sf' in param_name
                    ],
                    size=form.cleaned_data.get('size'),
                    estimate='предварительная',
                )
                result_form = ResultForm(initial={'pm': str(result.pm), 'tm': str(result.tm)})

                request.session['cocomo_3'] = request.POST
                request.session['cocomo_3_result'] = {'pm': str(result.pm), 'tm': str(result.tm)}

                context = {
                    'result_form': result_form,
                    'form': form,
                    'calculator_name': calculator_name,
                }
                return render(request, 'calculator/calculator.html', context)

            context = {
                'form': form,
                'calculator_name': calculator_name,
            }
            return render(request, 'calculator/calculator.html', context)

        elif kwargs.get('cocomo_version') == 4:
            calculator_name = 'COCOMO II (детальная оценка)'
            form = COCOMO2Form(request.POST, estimate='детальная')

            if form.is_valid():
                result = COCOMO2(
                    ems=[
                        form.cleaned_data[param_name]
                        for param_name in form.cleaned_data.keys()
                        if 'em' in param_name
                    ],
                    sfs=[
                        form.cleaned_data[param_name]
                        for param_name in form.cleaned_data.keys()
                        if 'sf' in param_name
                    ],
                    size=form.cleaned_data.get('size'),
                    estimate='детальная',
                )
                result_form = ResultForm(initial={'pm': str(result.pm), 'tm': str(result.tm)})

                request.session['cocomo_4'] = request.POST
                request.session['cocomo_4_result'] = {'pm': str(result.pm), 'tm': str(result.tm)}

                context = {
                    'result_form': result_form,
                    'form': form,
                    'calculator_name': calculator_name,
                }
                return render(request, 'calculator/calculator.html', context)

            context = {
                'form': form,
                'calculator_name': calculator_name,
            }
            return render(request, 'calculator/calculator.html', context)

        else:
            return HttpResponseRedirect(reverse('calculator:main'))


class MainView(View):
    def get(self, request, *_, **__):
        return render(request, 'calculator/main.html')
