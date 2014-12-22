# Create your views here.
#from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.shortcuts import render, get_object_or_404
from Apps.Asset.Property_asset.models import *
from Apps.Asset.Penghapusan.models import *
from Apps.Asset.Penjualan.models import *
from datetime import datetime
from Apps.Asset.forms import *
from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User

def login(request):
	if request.method == 'POST':
		try:
			c = Ms_customer.objects.get(username=request.POST['username'])
			if c.password == request.POST['password'] and c.customer_verified == True:
				request.session['member_id'] = c.id
				request.session['uname'] = c.username
				request.session['name'] = c.customer_name
				request.session['verified'] = c.customer_verified
				return render(request, 'templateasset/login_success.html',{'c':c})
			else : 
				return render(request, 'templateasset/login_fail.html')
		except:
			 return render(request, 'templateasset/login_fail.html')
	else:
		return render(request,'templateasset/login.html')

def logout(request):
	try:
		del request.session['member_id']
		del request.session['uname']
		del request.session['name']
		del request.session['verified']
	except KeyError:
		pass
	return render(request,'templateasset/logout.html')

def index(request):
	try:
		mem_id = request.session['member_id']
	except:
		mem_id = ''
	if mem_id == '':
		return render(request, 'templateasset/login_required.html')
	else:
		c = Ms_customer.objects.get(id=mem_id)
		post = Procurement.objects.filter(published=True)
		jml = post.count()
		return render(request,'templateasset/index.html',{'post':post, 'jml':jml,'c':c})

def contact_person(request):
	try:
		mem_id = request.session['member_id']
	except:
		mem_id = ''
	if mem_id == '':
		return render(request, 'templateasset/login_required.html')
	else:
		c = Ms_customer.objects.get(id=mem_id)
		post = Procurement.objects.filter(published=True)
		jml = post.count()
		return render(request,'templateasset/contact.html',{'post':post, 'jml':jml,'c':c})

		
def detail(request, slug):	
	try:
		mem_id = request.session['member_id']
	except:
		mem_id = ''
	if mem_id == '':
		return render(request, 'templateasset/login_required.html')
	else:
		detail = get_object_or_404(Procurement,slug=slug)
		ada = False
		try:
			p = Customer_proc.objects.get(customer__id=mem_id, procurement__slug=slug)
			ada = True
		except:
			pass
		return render(request,'templateasset/detail.html',{'detail':detail,'ada':ada})

#def detail(request, slug):	
#	detail = get_object_or_404(Procurement,slug=slug)
	
#	return render(request,'templateasset/detail.html',{'detail':detail})	
	
def update_profil(request): # ================ update Profil
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request, 'templateasset/login_required.html')
	else:	
		c = Ms_customer.objects.get(id=m_id)
		return render(request, 'templateasset/update_profil.html',{'c':c})	
		
def allproc(request): # ================ proc announcement
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request,'templateasset/login_required.html')
	else:	
		detail = Procurement.objects.filter(published=True)
		return render(request,'templateasset/Procurement/allproc.html',{'detail':detail})
			
		
def register(request):
	if request.method == 'POST':
		form = Register(request.POST)
		if form.is_valid():
			member = form.save()
			return render(request,'templateasset/Register/reg_success.html')
	else:
		form = Register()
	return render_to_response('templateasset/Register/registration_form.html', {'form':form}, context_instance=RequestContext(request))

def customerprog(request):
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request, 'templateasset/login_required.html')
		
	else:
	
		proc = Procurement.objects.get(slug=slug)
		cus = Ms_customer.objects.get(id=m_id)
		bid_value = Bidding.objects.get(bid_value=m_id)
		add_date = Customer_proc.objects.get(add_date=m_add_date)
		
		
		return render(request, 'templateasset/customerproc.html',{'proc':proc, 'cus':cus,'bid_value':bid_value,'add_date':add_date})

def daftarproc(request,slug):
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request,'templateasset/login_required.html')
	else:
		m = Ms_customer.objects.get(id=m_id)
		p = Procurement.objects.get(slug=slug)
		daftar = Customer_proc(customer=m, procurement=p)
		daftar.save()
		return render (request, 'templateasset/Procurement/register_success.html')
	
def bidding(request,slug):
	try:
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '' :
		return render(request,'templateasset/login_required.html')
	else:
		m = Ms_customer.objects.get(id=m_id)
		p = Procurement.objects.get(slug=slug)
		date = Bidding.objects.get(msg_add_date=m_msg_add_date)
		msg = Bidding.objects.get(msg=msg)

		return render(request,'templateasset/Bid/bidding.html',{'p':p,'m':m,'msg':msg})

def value(request,slug):
	try:
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request,'templateasset/login_required.html')
	else:
		p = Procurement.objects.get(slug=slug)	
		m = Customer_proc.objects.get(procurement__slug=slug, customer__id=m_id)
		b = Bidding.objects.filter(custom_proc=m)
		if request.method == 'POST':
			form = Proc_register(request.POST or None, instance=m)
			if form.is_valid():
				form.save()
				destination = 'value/%(slug)s' % {'slug':slug}
				return render(request,'templateasset/Procurement/submit_success.html',{'destination':destination})
			#kate melaksanakan opo?
	#		val = Customer_proc.objects.get(bid_value=m_bid_value)
			#return nak success
		else:
			form = Proc_register(instance=m)
		return render_to_response('templateasset/Procurement/value.html',{'p':p,'b':b,'form':form,'slug':slug,'m':m}, context_instance=RequestContext(request))
		
def pengumuman(request): # ================ 
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request, 'templateasset/login_required.html')
	else:	
		p = Procurement.objects.all	()
				
	return render(request, 'templateasset/Procurement/pengumuman.html',{'p':p})

def post_message(request,id):
	cus = Customer_proc.objects.get(id=id) 
	msg = request.POST['msg']
	data = Bidding(custom_proc=cus, msg=msg, uname=cus.customer.username)
	data.save()
	proc = Procurement.objects.get(id=cus.procurement.id)
	destination = 'value/%(var)s' % {'var':proc.slug}
	return render(request, 'templateasset/Procurement/edit_success.html',{'destination':destination})

def edit_profil(request):
	try :
		m_id = request.session['member_id']
	except:
		m_id = ''
		pass
	if m_id == '':
		return render(request, 'templateasset/login_required.html')
	else:
		m_id = get_object_or_404(Ms_customer,id=request.session['member_id'])
		if request.method == 'POST':
			form = EditData(request.POST or None, instance=m_id)
			if form.is_valid():
				form.save()
				destination = 'update_profil'
				msg1 = 'Informasi Umum Berhasil Dirubah'	
				return render(request, 'templateasset/edit_profil_success.html',{'destination':destination,'msg1':msg1})
		else:
			form = EditData(instance=m_id)
		return render_to_response('templateasset/edit_customer.html', {'form':form}, context_instance=RequestContext(request))
	
