__author__ = 'FARID ILHAM Al-Q'

from django.shortcuts import render_to_response
from django.template import RequestContext
from Apps.Inventory.product.models import Category, ProductItem
from django.http import HttpResponseRedirect


def index(request):
    data = Category.objects.all()
    ctx = {
        'item': data
    }
    return render_to_response('product/category.html', ctx, context_instance=RequestContext(request))


def item(request, id):
    item = ProductItem.objects.filter(category=id)
    ctx = {
        'botol': item
    }
    return render_to_response('product/product_item.html', ctx, context_instance=RequestContext(request))


def detail_item(request, id):
    detail = ProductItem.objects.get(id=id)
    ctx = {
        'detail': detail
    }
    return render_to_response('product/product_item_detail.html', ctx, context_instance=RequestContext(request))





