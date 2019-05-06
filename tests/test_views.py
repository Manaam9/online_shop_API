import json

from somemart.models import Item, Review


class TestItemView(object):

    def test_post_item(self, client, db):
        """ /api/v1/goods/ (POST) - saves product to the database. """

        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Cheese "Russian"',
            'description': 'Very delicious cheese.',
            'price': 100
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Object was saved to the database.
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Cheese "Russian"'
        assert item.description == 'Very delicious cheese'
        assert item.price == 100


class TestReviewView(object):

    def test_post_review(self, client, db, item_id):
        """ /api/v1/goods/:id/reviews/ (POST) - creates product Review, where :id - is product id. """

        url = 'api/v1/goods/<int:item_id>/reviews/'
        data = json.dumps({
            "text": "Best. Cheese. Ever.",
            "grade": 9
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        # Object was saved to the database.
        review = Review.objects.get(item__review__item_id=item_id)
        assert review.text == 'Best. Cheese. Ever.'
        assert review.grade == '9'
