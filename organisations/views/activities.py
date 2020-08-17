from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from audit_trail import service as audit_trail_service
from audit_trail.models import Audit
from audit_trail.serializers import AuditSerializer
from api.conf.authentication import GovAuthentication
from organisations.models import Organisation, Site


class OrganisationActivityView(APIView):
    authentication_classes = (GovAuthentication,)

    def get(self, request, pk):
        organisation = Organisation.objects.get(pk=pk)
        audit_trail_qs = audit_trail_service.get_activity_for_user_and_model(
            user=request.user, object_type=organisation
        )

        return JsonResponse(
            data={"activity": AuditSerializer(audit_trail_qs, many=True).data}, status=status.HTTP_200_OK
        )


class SitesActivityView(APIView):
    authentication_classes = (GovAuthentication,)

    def get(self, request, pk):
        organisation = Organisation.objects.get(pk=pk)
        site_ids = [
            str(site_id) for site_id in Site.objects.filter(organisation=organisation).values_list("id", flat=True)
        ]

        audit_trail_qs = Audit.objects.filter(
            target_content_type=ContentType.objects.get_for_model(Site), target_object_id__in=site_ids
        )

        return JsonResponse(
            data={"activity": AuditSerializer(audit_trail_qs, many=True).data}, status=status.HTTP_200_OK
        )
