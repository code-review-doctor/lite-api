import json

import reversion
from django.db import transaction
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from applications.models import Application
from applications.serializers import ApplicationBaseSerializer, ApplicationUpdateSerializer
from cases.models import Case
from conf.authentication import PkAuthentication
from drafts.libraries.get_draft import get_draft_with_organisation
from organisations.libraries.get_organisation import get_organisation_by_user
from queues.models import Queue


class ApplicationList(APIView):
    authentication_classes = (PkAuthentication,)
    """
    List all applications, or create a new application from a draft.
    """
    def get(self, request):
        organisation = get_organisation_by_user(request.user)

        applications = Application.objects.filter(organisation=organisation).order_by('created_at')
        serializer = ApplicationBaseSerializer(applications, many=True)
        return JsonResponse(data={'applications': serializer.data},
                            safe=False)

    @transaction.atomic
    def post(self, request):
        submit_id = json.loads(request.body).get('id')

        with reversion.create_revision():

            # Get Draft
            draft = get_draft_with_organisation(submit_id, get_organisation_by_user(request.user))

            # Create an Application object corresponding to the draft
            application = Application(id=draft.id,
                                      name=draft.name,
                                      activity=draft.activity,
                                      destination=draft.destination,
                                      usage=draft.usage,
                                      created_at=draft.created_at,
                                      last_modified_at=draft.last_modified_at,
                                      organisation=draft.organisation,
                                      )

            application.save()

            # Store meta-information.
            reversion.set_user(request.user)
            reversion.set_comment("Created Application Revision")

            # Delete draft
            draft.delete()

            # Create a case
            case = Case(application=application)
            case.save()

            # Add said case to default queue
            queue = Queue.objects.get(pk='00000000-0000-0000-0000-000000000001')
            queue.cases.add(case)
            queue.save()

            serializer = ApplicationBaseSerializer(application)
            return JsonResponse(data={'application': serializer.data},
                                status=status.HTTP_201_CREATED)


class ApplicationDetail(APIView):
    """
    Retrieve, update or delete a application instance.
    """
    def get_object(self, pk):
        try:
            application = Application.objects.get(pk=pk)
            return application
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationBaseSerializer(application)
        return JsonResponse(data={'status': 'success', 'application': serializer.data})

    def put(self, request, pk):
        with reversion.create_revision():
            data = JSONParser().parse(request)
            serializer = ApplicationUpdateSerializer(self.get_object(pk), data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data={'application': serializer.data},
                                    status=status.HTTP_200_OK)
            return JsonResponse(data={'errors': serializer.errors},
                                status=400)
