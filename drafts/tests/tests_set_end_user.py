from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from drafts.models import Draft
from test_helpers.clients import DataTestClient
from test_helpers.org_and_user_helper import OrgAndUserHelper


class EndUserOnDraftTests(DataTestClient):

    def setUp(self):
        super().setUp()
        self.org = self.test_helper.organisation
        self.primary_site = self.org.primary_site
        self.draft = OrgAndUserHelper.complete_draft('Goods test', self.org)
        self.url = reverse('drafts:end_user', kwargs={'pk': self.draft.id})

    @parameterized.expand([
        'government',
        'commercial',
        'other'
    ])
    def test_set_end_user_on_draft_successful(self, data_type):
        data = {
            'name': 'Government',
            'address': 'Westminster, London SW1A 0AA',
            'country': 'United Kingdom',
            'type': data_type,
            'website': 'https://www.gov.uk'
        }
        self.draft = Draft.objects.get(pk=self.draft.id)

        response = self.client.post(self.url, data, **self.headers)

        self.draft.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.draft.end_user.name, data['name'])
        self.assertEqual(self.draft.end_user.address, data['address'])
        self.assertEqual(self.draft.end_user.country, data['country'])
        self.assertEqual(self.draft.end_user.type, data_type)
        self.assertEqual(self.draft.end_user.website, data['website'])

    @parameterized.expand([
        [{}],
        [{
            'name': 'Lemonworld Org',
            'address': '3730 Martinsburg Rd, Gambier, Ohio',
            'country': 'United States of America',
            'website': 'https://www.americanmary.com'
        }],
        [{
            'name': 'Lemonworld Org',
            'address': '3730 Martinsburg Rd, Gambier, Ohio',
            'country': 'United States of America',
            'type': 'business',
            'website': 'https://www.americanmary.com'
        }],
    ])
    def test_set_end_user_on_draft_failure(self, data):
        self.draft = Draft.objects.get(pk=self.draft.id)

        response = self.client.post(self.url, data, **self.headers)

        self.draft.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.draft.end_user, None)
