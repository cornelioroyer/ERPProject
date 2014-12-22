from django.shortcuts import render
from Apps.Distribution.order.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def print_so_admin(request, id):
    jml = total = 0
    data = SalesOrder.objects.get(id=id)
    item = {}
    try:
        item = OrderItem.objects.get(so_reff__id=id)
    except:
        pass
    return render(request, 'admin/order/report/so.html', {'data':data,'item':item,'jml':jml,'total':total})