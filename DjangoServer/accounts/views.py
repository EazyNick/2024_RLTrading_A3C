from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class AccountHomeView(TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request, *args, **kwargs):
        logger.info("AccountHomeView GET request received")
        return super().get(request, *args, **kwargs)
