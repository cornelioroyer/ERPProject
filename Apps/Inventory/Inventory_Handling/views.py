from django.shortcuts import render

from Apps.Inventory.Inventory_Handling.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext, loader

@login_required
def print_data_admin(request, id):
     data = master_commodity.objects.get(id=id)
     return render(request, 'templateinv/mc.html', {'data':data})