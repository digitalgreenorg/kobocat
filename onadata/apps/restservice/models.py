# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy

from onadata.apps.logger.models.xform import XForm
from onadata.apps.restservice import SERVICE_CHOICES


@python_2_unicode_compatible
class RestService(models.Model):

    class Meta:
        app_label = 'restservice'
        unique_together = ('service_url', 'xform', 'name')

    service_url = models.URLField(ugettext_lazy("Service URL"))
    xform = models.ForeignKey(XForm, related_name="restservices", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES)

    def __str__(self):
        return "%s:%s - %s" % (self.xform, self.long_name, self.service_url)

    def get_service_definition(self):
        m = __import__(''.join(['onadata.apps.restservice.services.',
                       self.name]),
                       globals(), locals(), ['ServiceDefinition'])
        return m.ServiceDefinition

    @property
    def long_name(self):
        sv = self.get_service_definition()
        return sv.verbose_name
