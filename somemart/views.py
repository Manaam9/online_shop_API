import json

import base64

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from somemart.shemas import ItemSchema, ReviewSchema
from .models import Item, Review

from marshmallow.exceptions import MarshmallowError


@method_decorator(csrf_exempt, name='dispatch')  # delete this string on production
class AddItemView(View):
    """ Item creation View. """

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            item = schema.load(document).data
            auth = document['Authorization'].split()
            if len(auth) == 2:
                try:
                    username, password = base64.b64decode(auth[1].encode('ascii')).decode('utf-8').split(":")
                    user = authenticate(username=username, password=password)
                    if user.is_staff:
                        item.save()
                    else:
                        return HttpResponse(status=403)
                except Exception:
                    return HttpResponse(status=401)
            else:
                return HttpResponse(status=401)

        except Item.DoesNotExist:
            return HttpResponse({'errors': 'There is no product with such id.'}, status=404)
        except KeyError:
            return HttpResponse({'errors': 'Required field is missing.'}, status=400)
        except json.JSONDecodeError:
            return HttpResponse({'errors': 'Invalid JSON.'}, status=400)
        except (MarshmallowError, AssertionError):
            return HttpResponse({'errors': 'Validation error.'}, status=400)

        data = {"id": item.pk}
        return JsonResponse(data, status=201)


@method_decorator(csrf_exempt, name='dispatch')  # delete this string on production
class PostReviewView(View):
    """ Review creation View. """

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            review = schema.load(document).data
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse({'errors': 'There is no product with such id.'}, status=404)
        except KeyError:
            return HttpResponse({'errors': 'Required field is missing.'}, status=400)
        except json.JSONDecodeError:
            return HttpResponse({'errors': 'Invalid JSON.'}, status=400)
        except (MarshmallowError, AssertionError):
            return HttpResponse({'errors': 'Validation error.'}, status=400)

        data = {"id": item.pk}
        return JsonResponse(data, status=201)


@method_decorator(csrf_exempt, name='dispatch')  # delete this string on production
class GetItemView(View):
    """
    View for getting product information.

    Returns main information about product and last 5 product reviews.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse({'errors': 'There is no product with such id.'}, status=404)
        schema = ItemSchema()
        data = schema.dump(item).data
        # gets the latest 5 product reviews
        reviews = Review.objects.filter(item=item_id).order_by('-id')[:5]
        schema = ReviewSchema(many=True)
        data['reviews'] = schema.dump(reviews).data
        return JsonResponse(data, status=200)

