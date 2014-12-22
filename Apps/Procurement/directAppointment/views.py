from Apps.Procurement.directAppointment.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required
def print_rq_admin(request, id):
	data = get_object_or_404(Bidding_Request, id=id)
	jml = 0
	try:
		item = Bidding_Request_Item.objects.filter(bidding_request__id=id)
		jml = item.count()
	except:
		pass
	return render(request, 'templatesproc/report/rq.html', {'data':data,'item':item,'jml':jml})