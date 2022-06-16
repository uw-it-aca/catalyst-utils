# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from userservice.user import UserService
from persistent_message.models import Message


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = UserService().get_user()
        context['signout_url'] = reverse('saml_logout')
        context['messages'] = []

        for message in Message.objects.active_messages():
            if 'message_level' not in context:
                context['message_level'] = message.get_level_display().lower()
            context['messages'].append(message.render())

        return context
