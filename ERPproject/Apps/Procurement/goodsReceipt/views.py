from Apps.Procurement.goodsReceipt.models import *
from Apps.Procurement.purchaseOrder.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required
def print_gr_admin(request, id):
    data = Goods_Receipt.objects.get(id=id)
    return render(request, 'templatesproc/report/gr.html', {'data':data})
