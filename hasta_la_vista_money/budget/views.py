from django.views.generic import TemplateView


class BudgetView(TemplateView):
    template_name = 'budget.html'
