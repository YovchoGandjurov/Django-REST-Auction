from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework import response
from django.contrib.auth.models import User

from accounts.models import Profile
from .models import Auction
import datetime


def get_date(type, days):
    if type == 'add':
        date = datetime.date.today() + datetime.timedelta(days=2)
        return date
    elif type == 'sub':
        date = datetime.date.today() - datetime.timedelta(days=2)
        return date
    return None


class AuctionTestCase(APITestCase):
    auctions_url = '/api/auctions/'

    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user_name",
            "password": "123",
            "email": "test@test.te",
            "first_name": "first",
            "last_name": "last"
        }
        self.profile_data = {"language": "BG"}

        self.user = User.objects.create(**self.user_data)
        self.profile = Profile.objects.create(
                user=self.user, **self.profile_data)

        self.client.force_authenticate(self.user)

        self.auction_data = {
            "title": "title test",
            "description": "description test",
            "initial_price": "200",
            "closing_date": get_date('add', 4),
            "step": "20",
        }

        self.create_auction = self.client.post(self.auctions_url + "create/",
                                               self.auction_data,
                                               format='json')
        self.auction = Auction.objects.first()

    def test_create_auction(self):
        auction = Auction.objects.get(
            owner_id=self.create_auction.data['owner']
        )
        edit_url = self.auctions_url + str(auction.id) + "/edit/"
        get_response = self.client.get(edit_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_unauth_user_create_auction(self):
        self.client.logout()
        create_auction = self.client.post(self.auctions_url + "create/",
                                          self.auction_data,
                                          format='json')
        self.assertTrue(create_auction.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_auction_with_past_date(self):
        auction_data = self.auction_data
        auction_data['closing_date'] = get_date('sub', 5)
        create_auction = self.client.post(self.auctions_url + "create/",
                                          auction_data,
                                          format='json')
        self.assertTrue(create_auction.status_code != status.HTTP_200_OK)

    def test_user_edit_own_auction(self):

        # test user reach edit url
        auction = Auction.objects.first()
        edit_url = self.auctions_url + str(auction.id) + '/edit/'
        get_request = self.client.get(edit_url)
        self.assertEqual(get_request.status_code, status.HTTP_200_OK)

        # test closing_date is updated after put
        auction_data = self.auction_data
        auction_data['closing_date'] = get_date('sub', 2)
        edit_auction = self.client.put(edit_url,
                                       auction_data,
                                       format='json')
        auction = Auction.objects.first()
        self.assertEqual(auction.closing_date, get_date('sub', 2))

        # test user if can see closed auction
        get_request = self.client.get(self.auctions_url)
        dict_result = get_request.data.__dict__
        self.assertTrue(len(dict_result) == 0)

        # test the auction ends automatically
        auction = Auction.objects.first()
        self.assertEqual(auction.status, 'Closed')

    def test_user_can_delete_own_auction(self):
        del_url = self.auctions_url + str(self.auction.id) + '/edit/'
        delete_request = self.client.delete(del_url)
        self.assertTrue(Auction.objects.count() == 0)

    def test_make_bid_less_than_step_or_with_string(self):
        bid_url = self.auctions_url + str(self.auction.id) + '/'
        request = self.client.patch(bid_url, {"bid": 'null'}, format='json')
        self.assertNotEqual(request.status_code, status.HTTP_200_OK)

        number = int(self.auction.step) - 1
        request = self.client.patch(bid_url, {"bid": number}, format='json')
        self.assertNotEqual(request.status_code, status.HTTP_200_OK)

    def test_unauth_user_can_bid(self):
        self.client.logout()
        bid_url = self.auctions_url + str(self.auction.id) + '/'
        number = int(self.auction.step) + 1
        request = self.client.patch(bid_url, {"bid": number}, format='json')
        self.assertNotEqual(request.status_code, status.HTTP_200_OK)

    def test_post_category(self):
        url = self.auctions_url + '/category/'
        request = self.client.post(url, {"name": "Technology"}, format='json')
        self.assertNotEqual(request.status_code, status.HTTP_200_OK)
