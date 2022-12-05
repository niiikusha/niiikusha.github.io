from django.urls import path

from calculator.views import CalculatorView, MainView

app_name = 'calculator'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('calculator/<int:cocomo_version>', CalculatorView.as_view(), name='calculator'),
]
