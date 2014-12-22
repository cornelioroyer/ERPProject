# Create your views here.
from Apps.Asset.Master.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext, loader


@login_required
def print_master(request, id):
    jml = total = 0
    data = Ms_asset.objects.all()
    item= {}
    try:
        item = Ms_asset.objects.all()
        jml += item.count()
    except:
        pass

    return render(request, 'templatesproc/report/po.html', {'data':data,'item':item,'jml':jml})

def reportaset(request):
    user = Group.objects.get(user=request.user)
    if user.name == 'staff' or user.name == 'manager':
        data = {}
        n = total = 0
        key = ''
        if request.method == 'POST':
            key = request.POST.get('keyword','')
            try :
                data = Ms_asset.objects.filter(plan_month__contains=request.POST.get('keyword',''))
                n = data.count
                for d in data: total = total + float(d.tot())
            except : pass
        return render_to_response('templateasset/report/reportasset.html',{'data':data,'n':n,'key':key,'total':total}, RequestContext(request,{}),)
    else:
        return render_to_response('templatesproc/report/acces_denied.html', RequestContext(request,{}),)
