from django.urls import reverse
from rest_framework import status

from applications.enums import LicenceDuration
from applications.libraries.licence import get_default_duration
from conf.constants import GovPermissions
from static.statuses.enums import CaseStatusEnum
from static.statuses.libraries.get_case_status import get_case_status_by_status
from test_helpers.clients import DataTestClient
from users.models import Role
from lite_content.lite_api import strings


class FinaliseApplicationTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.standard_application = self.create_standard_application(self.organisation)
        self.submit_application(self.standard_application)
        self.url = reverse("applications:finalise", kwargs={"pk": self.standard_application.id})
        self.role = Role.objects.create(name="test")

    def test_gov_user_finalise_permission_error(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([])
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gov_user_finalise_application_success(self):
        self.assertEqual(self.standard_application.licence_duration, None)

        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.standard_application.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.standard_application.status, get_case_status_by_status(CaseStatusEnum.FINALISED))
        self.assertEqual(self.standard_application.licence_duration, data["licence_duration"])

    def test_gov_use_set_duration_permission_denied(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"licence_duration": 13}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"errors": [strings.Applications.Finalise.Error.SET_DURATION_PERMISSION]})

    def test_invalid_duration_data(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set(
            [GovPermissions.MANAGE_FINAL_ADVICE.name, GovPermissions.MANAGE_LICENCE_DURATION.name]
        )
        self.gov_user.save()

        data = {"licence_duration": LicenceDuration.MAX.value + 1}
        response = self.client.put(self.url, data=data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"errors": {"non_field_errors": [strings.Applications.Finalise.Error.DURATION_RANGE]}}
        )

    def test_default_duration_no_permission_application_finalised_success(self):
        self.gov_user.role = self.role
        self.gov_user.role.permissions.set([GovPermissions.MANAGE_FINAL_ADVICE.name])
        self.gov_user.save()

        data = {"licence_duration": get_default_duration(self.standard_application)}
        response = self.client.put(self.url, data=data, **self.gov_headers)
        self.standard_application.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.standard_application.licence_duration, data["licence_duration"])
