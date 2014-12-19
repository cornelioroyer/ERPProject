# Create your views here.
from Apps.Hrm.Salary.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import Group
from django.template import RequestContext, loader

def reportsalary(request):
	user = Group.objects.get(user=request.user)
	if user.name == 'kadep_hrm' or user.name == 'kabag_hrm' or user.name == 'kasie_hrm' or user.name == 'staff_hrm':
		data = {}
		n = total = 0
		key = ''
		if request.method == 'POST':
			key = request.POST.get('keyword','')
			try :
				data = Header_Salary.objects.filter(plan_month__contains=request.POST.get('keyword',''))
				n = data.count
				for d in data: total = total + float(d.tot())
			except : pass
		return render_to_response('templatesalary/report/reportsalary.html',{'data':data,'n':n,'key':key,'total':total}, RequestContext(request,{}),)
	else: 
		return render_to_response('templatesproc/report/acces_denied.html', RequestContext(request,{}),)

@login_required
def print_gaji_admin(request, id):
	data = Header_Salary.objects.get(id=id)
	try:
		gaji = Salary_Employee.objects.get(header__id=id)
		cut = Cut_Of_Salary.objects.get(header__id=id)
	except:pass
	total = Total_Salary.objects.get(header__id=id)
	return render(request, 'templatesalary/cetak/gaji.html', {'data':data,'gaji':gaji, 'cut':cut, 'tot':total,})