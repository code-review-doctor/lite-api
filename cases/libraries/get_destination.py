from django.http import Http404

from parties.models import Party
from static.countries.models import Country


def get_destination(pk):
    try:
        destination = Country.include_special_countries.get(pk=pk)
    except Country.DoesNotExist:
        try:
            destination = Party.objects.get(pk=pk)
        except Party.DoesNotExist:
            raise Http404
    return destination
