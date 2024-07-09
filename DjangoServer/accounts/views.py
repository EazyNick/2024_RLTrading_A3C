from django.views.generic import TemplateView

class AccountHomeView(TemplateView):
    template_name = 'accounts/home.html'
