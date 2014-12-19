# Create your views here.
from django.shortcuts import render, get_object_or_404, render_to_response, HttpResponse
from Apps.Procurement.vendor.models import *
from Apps.Procurement.internal.models import *
from Apps.Procurement.property.models import *
from Apps.Procurement.purchaseOrder.models import *

from Apps.Hrm.Master_General.models import Department
from Apps.Accounting.CashBank.models import Budget
from Apps.Accounting.GeneralLedger.models import Ms_Fiscal_Years

from django.template import RequestContext, loader
from django.contrib.auth.models import User
from Apps.Procurement.forms import *
from django.core.paginator import *
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from collections import Counter
from filetransfers.api import prepare_upload, serve_file
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == '' or level == 'vendor':
		return render(request,'templatesproc/vendor/login_required.html')
	else :
		return render(request, 'templatesproc/internal/index.html',{'level':level,'uname':uname})
		
def rkb_page(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else :
			intnow += 1
		
		plan_id = '0'
		budget_ada = 0
		d = User_Intern.objects.get(username=uname)
		periode = 0
		total_all1 = 0
		total_all2 = 0
		total_all = 0
				
		try:
			budget = Budget.objects.filter(department=d.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		if budget_ada > 0:
			for bs in budget:
				b_id = bs.id
				b_value = bs.budget_value
				b_devided = bs.budget_devided
				
			strnow = str(intnow)
			
			if len(strnow) < 2 :
				strnow = '0%(strnow)s' % {'strnow' : strnow}
			bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
			
			bagi = int(b_value) / int(b_devided)
			bagian = 12 / int(b_devided)
			n = 1
			while n <= int(b_devided):
				temp = int(bagian) * n
				temp2 = (temp - int(bagian))+1
				if intnow <= temp and intnow >= temp2:
					periode = n
					while temp2 <= temp:
						strtemp2 = str(temp2)
						
						if len(strtemp2) < 2 :
							strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
						else :
							strnow = '%(strtemp2)s' % {'strtemp2' : strtemp2}
						bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
						try: 
							hr = Header_Purchase_Request.objects.get(department=d.department,request_month=bln)
							dr = Data_Purchase_Request.objects.filter(header_purchase_request_id=hr.id)
							for drs in dr:
								total_all1 += float(drs.request_total_price)
						except:
							pass

						try:
							hro = Header_Rush_Order.objects.get(department=d.department,ro_month=bln,ro_lock=True)
							dro = Data_Rush_Order.objects.filter(header_rush_order_id=hro.id)
							for dros in dro:
								total_all1 += float(dros.ro_total_price)
						except:
							pass
						temp2 = temp2 + 1
					
				n = n + 1
			
			try:
				hp = Header_Plan.objects.get(department=d.department,plan_month=bulan)
				dp = Data_Plan.objects.filter(header_plan_id=hp.id)
				for dps in dp:
					total_all2 += float(dps.plan_total_price)
			except:
				pass
			
			ada = 0
			h = {}
			try:
				h = Header_Plan.objects.filter(department=d.department,plan_month=bulan)
				ada = h.count()
				for hsl in h :
					request.session['plan_id'] = hsl.id
					if hsl.lock == True:
						total_all = total_all1
					else: total_all = total_all1 + total_all2 
			except:
				pass
			
			data = val = {}
			ada_data = n = 0
			total = 0
			if ada > 0 :
				try:
					data = Data_Plan.objects.filter(header_plan_id=request.session['plan_id'])
					ada_data = data.count()
					for datas in data:
						total += float(datas.plan_total_price)
						val[n] = float(datas.plan_total_price)
						n+=1
				except:
					pass
			
			sisa = float(bagi) - total_all
			intyear = str(intyear)
			return render(request,'templatesproc/internal/rkb_page.html', {'ada':ada,'d':d,'uname':uname,'bulan':bulan,'h':h,'data':data,'ada_data':ada_data,'total':total,
						'b_value':b_value,'b_devided':b_devided,'sisa':sisa,'bagi':bagi,'total_all':total_all,'periode':periode,'intyear':intyear})
		else: 
			return render(request, 'templatesproc/internal/warning.html')
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def make_rkb(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else : 
			intnow += 1
		
		strnow = str(intnow)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
		ada = True
		d = User_Intern.objects.get(username=uname)
		try:
			h = Header_Plan.objects.get(department=d.department,plan_month=bulan)
		except:
			ada = False
			pass
		if ada == True:
			return render(request,'templatesproc/internal/warning.html')
		else:
			f = Ms_Fiscal_Years.objects.get(Code=str(intyear))
			header = Header_Plan(department=d.department,plan_month=bulan,fiscal_year=f)
			header.save()
			target = 'rkb_page'
			return render(request,'templatesproc/internal/op_success.html', {'ada':ada,'d':d,'uname':uname,'target':target}) 
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def add_rkb(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		ada = True
		uname = request.session['uname']
		plan_id = request.session['plan_id']
		data = 'Item RKB'
		action = '/add_rkb/'
		if request.method == 'POST':
			form = DataPlan(request.POST)
			if form.is_valid():
				form.save()
				target = 'rkb_page'
				return render(request,'templatesproc/internal/op_success.html', {'uname':uname,'target':target})
		form = DataPlan(initial={'header_plan_id': plan_id})
		return render(request, 'templatesproc/internal/add.html', {'form':form, 'data':data,'uname':uname,'action':action})
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def edit_rkb(request,id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		ada = True
		uname = request.session['uname']
		plan_id = request.session['plan_id']
		d = get_object_or_404(Data_Plan,id=id)
		data = 'Edit Item RKB'
		action = '/edit_rkb/'+id+'/'
		total_rp = '0'
		total_price = '0'
		if request.method == 'POST':
			form = DataPlan(request.POST or None,request.FILES,instance=d)
			if form.is_valid():
				form.save()
				target = 'rkb_page'
				return render(request,'templatesproc/internal/op_success.html',{'target':target})
		form = DataPlan(initial={'header_plan_id': plan_id},instance=d)
		return render(request, 'templatesproc/internal/add.html', {'form':form, 'data':data,'uname':uname,'action':action})
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def del_rkb(request, id):
	try :
		level = request.session['level']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		Data_Plan.objects.filter(id=id).delete()
		return render(request, 'templatesproc/internal/op_success.html',{'target':target})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def lock_rkb(request, id):
	try :
		level = request.session['level']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		isimenu = 'vendor'
		d = get_object_or_404(Header_Plan,id=id)
		d.lock=True
		d.save()
		req = Header_Purchase_Request(department=d.department,request_month=d.plan_month,header_plan=d,fiscal_year=d.fiscal_year)
		req.save()
		
		isi = Data_Plan.objects.filter(header_plan_id=id)
		h_req = Header_Purchase_Request.objects.get(department=d.department,request_month=d.plan_month)
		for xx in isi:
			curr = Currency.objects.get(currency_symbol=xx.currency_id)
			g_type = Goods_Type.objects.get(goods_type_detail=xx.goods_type_id)
			uom = Unit_Of_Measure.objects.get(unit_of_measure_detail=xx.unit_of_measure_id)
			d_req = Data_Purchase_Request(header_purchase_request_id=h_req, request_goods_name=xx.plan_goods_name,request_used=xx.plan_used,
					request_amount=xx.plan_amount,request_unit_price=xx.plan_unit_price,request_total_rupiah=xx.plan_total_rupiah,
					request_total_price=xx.plan_total_price,request_detail=xx.plan_detail,currency_id=curr, goods_type_id= g_type,
					unit_of_measure_id=uom)
			d_req.save()
			target = 'rkb_page'
		return render(request, 'templatesproc/internal/op_success.html',{'target':target})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

# ================================================================= END of Rencana Kebutuhan Barang View ==================================================== ##		

def pp_page(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else :
			intnow += 1
		
		req_id = '0'
		budget_ada = 0
		d = User_Intern.objects.get(username=uname)
		periode = 0
		total_all = 0
				
		try:
			budget = Budget.objects.filter(department=d.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		if budget_ada > 0:
			for bs in budget:
				b_id = bs.id
				b_value = bs.budget_value
				b_devided = bs.budget_devided
				
			strnow = str(intnow)
			
			if len(strnow) < 2 :
				strnow = '0%(strnow)s' % {'strnow' : strnow}
			bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
			
			bagi = int(b_value) / int(b_devided)
			bagian = 12 / int(b_devided)
			n = 1
			while n <= int(b_devided):
				temp = int(bagian) * n
				temp2 = (temp - int(bagian))+1
				if intnow <= temp and intnow >= temp2:
					periode = n
					while temp2 <= temp:
						strtemp2 = str(temp2)
						
						if len(strtemp2) < 2 :
							strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
						else :
							strnow = '%(strtemp2)s' % {'strtemp2' : strtemp2}
						bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
						try: 
							hr = Header_Purchase_Request.objects.get(department=d.department,request_month=bln)
							dr = Data_Purchase_Request.objects.filter(header_purchase_request_id=hr.id)
							for drs in dr:
								total_all += float(drs.request_total_price)
						except:
							pass

						try:
							hro = Header_Rush_Order.objects.get(department=d.department,ro_month=bln,ro_lock=True)
							dro = Data_Rush_Order.objects.filter(header_rush_order_id=hro.id)
							for dros in dro:
								total_all += float(dros.ro_total_price)
						except:
							pass
						temp2 = temp2 + 1
					
				n = n + 1
			
			sisa = float(bagi) - total_all
			ada = review1 = review2 = review3 = agreement = 0
			h = {}
			try:
				h = Header_Purchase_Request.objects.filter(department=d.department,request_month=bulan)
				ada = h.count()
				for hsl in h :
					request.session['req_id'] = hsl.id
					if hsl.warehouse_review == "" :
						review1 = 1
					if hsl.financial_review == "" :
						review2 = 1
					if hsl.procurement_review == "" :
						review3 = 1
					if hsl.warehouse_agreement == True and hsl.financial_agreement == True and hsl.procurement_agreement == True:
						agreement = 1
			except:
				pass
			
			data = {}
			ada_data = 0
			total = 0
			if ada > 0 :
				try:
					data = Data_Purchase_Request.objects.filter(header_purchase_request_id=request.session['req_id'])
					ada_data = data.count()
					for datas in data:
						total += float(datas.request_total_price)
				except:
					pass
			intyear = str(intyear)
			return render(request,'templatesproc/internal/pp_page.html', {'ada':ada,'d':d,'uname':uname,'bulan':bulan,'h':h,'data':data,'ada_data':ada_data,'total':total,
						'b_value':b_value,'b_devided':b_devided,'sisa':sisa,'bagi':bagi,'total_all':total_all,'periode':periode,'intyear':intyear,
						'review1':review1,'review2':review2,'review3':review3,'agreement':agreement})
		else: 
			return render(request, 'templatesproc/internal/warning.html')
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def edit_pp(request,id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		ada = True
		uname = request.session['uname']
		req_id = request.session['req_id']
		d = get_object_or_404(Data_Purchase_Request,id=id)
		data = 'Edit Item PP'
		action = '/edit_pp/'+id+'/'
		total_rp = '0'
		total_price = '0'
		if request.method == 'POST':
			form = DataReq(request.POST or None,request.FILES,instance=d)
			if form.is_valid():
				form.save()
				target = 'pp_page'
				return render(request,'templatesproc/internal/op_success.html',{'target':target})
		form = DataReq(initial={'header_purchase_request_id': req_id},instance=d)
		return render(request, 'templatesproc/internal/add.html', {'form':form, 'data':data,'uname':uname,'action':action})
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def del_pp(request, id):
	try :
		level = request.session['level']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		Data_Purchase_Request.objects.filter(id=id).delete()
		target = 'pp_page'
		return render(request, 'templatesproc/internal/op_success.html',{'target':target})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')
		
# ================================================================= END of Permintaan Pembelian View ==================================================== ##

def ro_page(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else :
			intnow += 1
		
		ro_id = '0'
		budget_ada = 0
		d = User_Intern.objects.get(username=uname)
		periode = 0
		total_all = 0
				
		try:
			budget = Budget.objects.filter(department=d.department, year__Code=str(intyear))
			budget_ada = budget.count()
		except:
			pass
		
		if budget_ada > 0:
			for bs in budget:
				b_id = bs.id
				b_value = bs.budget_value
				b_devided = bs.budget_devided
				
			strnow = str(intnow)
			
			if len(strnow) < 2 :
				strnow = '0%(strnow)s' % {'strnow' : strnow}
			bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
			
			bagi = int(b_value) / int(b_devided)
			bagian = 12 / int(b_devided)
			n = 1
			while n <= int(b_devided):
				temp = int(bagian) * n
				temp2 = (temp - int(bagian))+1
				if intnow <= temp and intnow >= temp2:
					periode = n
					while temp2 <= temp:
						strtemp2 = str(temp2)
						
						if len(strtemp2) < 2 :
							strnow = '0%(strtemp2)s' % {'strtemp2' : strtemp2}
						else :
							strnow = '%(strtemp2)s' % {'strtemp2' : strtemp2}
						bln = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
						try: 
							hr = Header_Purchase_Request.objects.get(department=d.department,request_month=bln)
							dr = Data_Purchase_Request.objects.filter(header_purchase_request_id=hr.id)
							for drs in dr:
								total_all += float(drs.request_total_price)
						except:
							pass
						
						try:
							hro = Header_Rush_Order.objects.get(department=d.department,ro_month=bln,ro_lock=True)
							dro = Data_Rush_Order.objects.filter(header_rush_order_id=hro.id)
							for dros in dro:
								total_all += float(dros.ro_total_price)
						except:
							pass
						temp2 = temp2 + 1
					
				n = n + 1
			
			sisa = float(bagi) - total_all
			ada = review1 = review2 = review3 = agreement = maked = 0
			h = {}
			try:
				h = Header_Rush_Order.objects.filter(department=d.department,ro_month=bulan, ro_lock=False, ro_type=1)
				ada = h.count()
				for hsl in h :
					request.session['ro_id'] = hsl.id
					if hsl.warehouse_review == "" :
						review1 = 1
					if hsl.financial_review == "" :
						review2 = 1
					if hsl.procurement_review == "" :
						review3 = 1
					if hsl.warehouse_agreement == True and hsl.financial_agreement == True and hsl.procurement_agreement == True:
						agreement = 1
			except:
				pass
			
			# ngecek PP sudah dibuat atau belum
			try:
				seek = Header_Purchase_Request.objects.filter(department=d.department,request_month=bulan)
				for ss in seek :
					if ss.request_lock == True:
						maked = 1
			except:
				pass
			
			data = {}
			ada_data = 0
			total = 0
			if ada > 0 :
				try:
					data = Data_Rush_Order.objects.filter(header_rush_order_id=request.session['ro_id'])
					ada_data = data.count()
					for datas in data:
						total += float(datas.ro_total_price)
				except:
					pass
			total_plus = sisa_plus = 0
			total_plus = total_all + total
			sisa_plus = sisa - total
			intyear = str(intyear)
			return render(request,'templatesproc/internal/ro_page.html', {'ada':ada,'d':d,'uname':uname,'bulan':bulan,'h':h,'data':data,'ada_data':ada_data,'total':total,
						'b_value':b_value,'b_devided':b_devided,'sisa':sisa,'bagi':bagi,'total_all':total_all,'periode':periode,'intyear':intyear,
						'review1':review1,'review2':review2,'review3':review3,'agreement':agreement,'maked':maked,'total_plus':total_plus,'sisa_plus':sisa_plus})
		else: 
			return render(request, 'templatesproc/internal/warning.html')
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def make_ro(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		now = datetime.now()
		nowmonth = now.strftime('%m')
		nowyear = now.strftime('%Y')
		intnow = int(nowmonth)
		intyear = int(nowyear)
		
		if intnow == 12:
			intnow = 1
			intyear += 1
		else : 
			intnow += 1
		
		strnow = str(intnow)
		
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		bulan = '%(intyear)s%(strnow)s' % {'intyear':intyear,'strnow':strnow}
		ada = True
		d = User_Intern.objects.get(username=uname)
		h = {}
		try:
			h = Header_Rush_Order.objects.get(department=d.department,ro_month=bulan,ro_type=1,ro_lock=False)
			n = h.count()
			if n == 0:
				ada = False
		except:
			pass
		if ada == False:
			return render(request,'templatesproc/internal/warning.html')
		else:
			f = Ms_Fiscal_Years.objects.get(Code=str(intyear))
			header = Header_Rush_Order(department=d.department,ro_type=1,fiscal_year=f)
			header.save()
			target = 'ro_page'
			return render(request,'templatesproc/internal/op_success.html', {'target':target}) 
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def sent_ro(request, id):
	try :
		level = request.session['level']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		d = get_object_or_404(Header_Rush_Order,id=id)
		d.ro_sent=True
		d.ro_type=1
		d.save()
		target = 'ro_page'
		return render(request, 'templatesproc/internal/op_success.html',{'target':target})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def add_ro(request):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		ada = True
		uname = request.session['uname']
		ro_id = request.session['ro_id']
		ro = Header_Rush_Order.objects.get(id=ro_id)
		data = 'Item Rush Order'
		action = '/add_ro/'
		if request.method == 'POST':
			form = DataRo(request.POST)
			if form.is_valid():
				form.save()
				target = 'ro_page'
				return render(request,'templatesproc/internal/op_success.html', {'uname':uname,'target':target})
		form = DataRo(initial={'header_rush_order_id': ro})
		return render(request, 'templatesproc/internal/add.html', {'form':form, 'data':data,'uname':uname,'action':action})
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def edit_ro(request,id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		ada = True
		uname = request.session['uname']
		ro_id = request.session['ro_id']
		d = get_object_or_404(Data_Rush_Order,id=id)
		data = 'Edit Item RO'
		action = '/edit_ro/'+id+'/'
		if request.method == 'POST':
			form = DataRo(request.POST or None,request.FILES,instance=d)
			if form.is_valid():
				form.save()
				target = 'ro_page'
				return render(request,'templatesproc/internal/op_success.html',{'target':target})
		form = DataRo(initial={'header_rush_order_id': ro_id},instance=d)
		return render(request, 'templatesproc/internal/add.html', {'form':form, 'data':data,'uname':uname,'action':action})
	else :
		return render(request, 'templatesproc/vendor/login_required.html',{'level':level})

def del_ro(request, id):
	try :
		level = request.session['level']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		Data_Rush_Order.objects.filter(id=id).delete()
		target = 'ro_page'
		return render(request, 'templatesproc/internal/op_success.html',{'target':target})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')
# ========================================================== END of Rush order ==================================== #

# ========================================================== Start of History  ==================================== #
def hist_rkb(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		d = User_Intern.objects.get(username=uname)
		hist_of = 'Rencana Kebutuhan Barang'
		s = key = s2 = key2 = ''
		enter = enter2 = False
		data = dtr = {}
		if id == '1':
			data = Header_Plan.objects.filter(department=d.department,lock=True).order_by('-plan_month')
			dtr = Data_Plan.objects.filter(header_plan_id__department=d.department,header_plan_id__lock=True).order_by('-header_plan_id__plan_month')
		
		if id == '2':
			try:
				s = request.POST['com_sort']
				if request.POST['keyword']=='Pencarian Kode Bulan' or request.POST['keyword']=='':
					key = ''
				else:
					key = request.POST['keyword']
			except:
				key = request.session['key']
				s = request.session['s']
			request.session['key'] = key
			request.session['s'] = s
			enter = True
			if s == 'Terbaru':
				data = Header_Plan.objects.filter(department=d.department, lock=True, plan_month__contains=key).order_by('-plan_month')
			else: data = Header_Plan.objects.filter(department=d.department, lock=True, plan_month__contains=key).order_by('plan_month')
			dtr = Data_Plan.objects.filter(header_plan_id__department=d.department,header_plan_id__lock=True).order_by('-header_plan_id__plan_month')
		
		if id == '3':
			try:
				s2 = request.POST['com_sort2']
				if request.POST['keyword2']=='Pencarian nama barang' or request.POST['keyword2']=='':
					key2 = ''
				else:
					key2 = request.POST['keyword2']
			except:
				key2 = request.session['key2']
				s2 = request.session['s2']
			request.session['key2'] = key2
			request.session['s2'] = s2
			enter2 = True
			if s2 == 'Terbaru':
				dtr = Data_Plan.objects.filter(header_plan_id__department=d.department,header_plan_id__lock=True,
						plan_goods_name__contains=key2).order_by('-header_plan_id__plan_month')
			else: dtr = Data_Plan.objects.filter(header_plan_id__department=d.department,header_plan_id__lock=True,
						plan_goods_name__contains=key2).order_by('header_plan_id__plan_month')
			data = Header_Plan.objects.filter(department=d.department,lock=True).order_by('-plan_month')
		
		all = Data_Plan.objects.filter(header_plan_id__department=d.department,header_plan_id__lock=True).order_by('-header_plan_id__plan_month')
		jml = list = []
		for alls in all:
			jml += [alls.plan_goods_name]
		
		list = Counter(jml).most_common()
		
		paginator = Paginator(data, 20)
		page = request.GET.get('page')
		try:
			rkb = paginator.page(page)
		except PageNotAnInteger:
			rkb = paginator.page(1)
		except EmptyPage:
			rkb = paginator.page(paginator.num_pages)
		
		paginator2 = Paginator(dtr, 20)
		page2 = request.GET.get('page_all')
		try:
			dr = paginator2.page(page2)
		except PageNotAnInteger:
			dr = paginator2.page(1)
		except EmptyPage:
			dr = paginator2.page(paginator2.num_pages)
		
		paginator3 = Paginator(list, 20)
		page3 = request.GET.get('page_count')
		try:
			lst = paginator3.page(page3)
		except PageNotAnInteger:
			lst = paginator3.page(1)
		except EmptyPage:
			lst = paginator3.page(paginator3.num_pages)
		return render(request, 'templatesproc/internal/list_rkb.html',{'hist_of':hist_of,'rkb':rkb,'key':key,'s':s,'enter':enter,'uname':uname,
						'dr':dr,'key2':key2,'s2':s2,'enter2':enter2,'lst':lst})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def detail_rkb(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		hs = get_object_or_404(Header_Plan,id=id)
		data = Data_Plan.objects.filter(header_plan_id__id=id)
		total = 0
		for d in data:
			total += float(d.plan_total_price)
		return render(request, 'templatesproc/internal/detail_rkb.html',{'hs':hs,'data':data,'total':total})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def hist_pp(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		d = User_Intern.objects.get(username=uname)
		hist_of = 'Permintaan Pembelian'
		s = key = s2 = key2 = ''
		enter = enter2 = False
		data = dtr = {}
		if id == '1':
			data = Header_Purchase_Request.objects.filter(department=d.department,request_lock=True).order_by('-request_month')
			dtr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=d.department,
					header_purchase_request_id__request_lock=True).order_by('-header_purchase_request_id__request_month')
		
		if id == '2':
			try:
				s = request.POST['com_sort']
				if request.POST['keyword']=='Pencarian Kode Bulan' or request.POST['keyword']=='':
					key = ''
				else:
					key = request.POST['keyword']
			except:
				key = request.session['key']
				s = request.session['s']
			request.session['key'] = key
			request.session['s'] = s
			enter = True
			if s == 'Terbaru':
				data = Header_Purchase_Request.objects.filter(department=d.department, requestlock=True, request_month__contains=key).order_by('-request_month')
			else: data = Header_Purchase_Request.objects.filter(department=d.department, request_lock=True, request_month__contains=key).order_by('request_month')
			dtr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=d.department,header_purchase_request_id__request_lock=True).order_by('-header_purchase_request_id__request_month')
		
		if id == '3':
			try:
				s2 = request.POST['com_sort2']
				if request.POST['keyword2']=='Pencarian nama barang' or request.POST['keyword2']=='':
					key2 = ''
				else:
					key2 = request.POST['keyword2']
			except:
				key2 = request.session['key2']
				s2 = request.session['s2']
			request.session['key2'] = key2
			request.session['s2'] = s2
			enter2 = True
			if s2 == 'Terbaru':
				dtr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=d.department,header_purchase_request_id__request_lock=True,
						request_goods_name__contains=key2).order_by('-header_purchase_request_id__request_month')
			else: dtr = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=d.department,header_purchase_request_id__request_lock=True,
						request_goods_name__contains=key2).order_by('header_purchase_request_id__request_month')
			data = Header_Purchase_Request.objects.filter(department=d.department,request_lock=True).order_by('-request_month')
		
		all = Data_Purchase_Request.objects.filter(header_purchase_request_id__department=d.department,
				header_purchase_request_id__request_lock=True).order_by('-header_purchase_request_id__request_month')
		
		nama = ['','']
		jml = list = []
		"""
		for alls in all:
			for i in range(len(nama)):
				if [alls.request_goods_name] == [nama[i]]:
					nama[i+1] = str((int(nama[i+1]) + 1))
					break;
				else:
					if i == len(nama)-1:
						nama += [alls.request_goods_name]
						nama += '1'	
		list.append(dict(zip(nama, jml)))
		"""
		
		for alls in all:
			jml += [alls.request_goods_name]
		
		list = Counter(jml).most_common()
		
		
		paginator = Paginator(data, 20)
		page = request.GET.get('page')
		try:
			rkb = paginator.page(page)
		except PageNotAnInteger:
			rkb = paginator.page(1)
		except EmptyPage:
			rkb = paginator.page(paginator.num_pages)
		
		paginator2 = Paginator(dtr, 20)
		page2 = request.GET.get('page_all')
		try:
			dr = paginator2.page(page2)
		except PageNotAnInteger:
			dr = paginator2.page(1)
		except EmptyPage:
			dr = paginator2.page(paginator2.num_pages)
		
		paginator3 = Paginator(list, 20)
		page3 = request.GET.get('page_count')
		try:
			lst = paginator3.page(page3)
		except PageNotAnInteger:
			lst = paginator3.page(1)
		except EmptyPage:
			lst = paginator3.page(paginator3.num_pages)
		return render(request, 'templatesproc/internal/list_pp.html',{'hist_of':hist_of,'rkb':rkb,'key':key,'s':s,'enter':enter,'uname':uname,
						'dr':dr,'key2':key2,'s2':s2,'enter2':enter2,'list':list,'all':all,'nama':nama,'jml':jml,'lst':lst})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def detail_pp(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		hs = get_object_or_404(Header_Purchase_Request,id=id)
		data = Data_Purchase_Request.objects.filter(header_purchase_request_id__id=id)
		total = 0
		for d in data:
			total += float(d.request_total_price)
		return render(request, 'templatesproc/internal/detail_pp.html',{'hs':hs,'data':data,'total':total})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def hist_ro(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		d = User_Intern.objects.get(username=uname)
		hist_of = 'Rush Order'
		s = key = s2 = key2 = ''
		enter = enter2 = False
		data = dtr = {}
		if id == '1':
			data = Header_Rush_Order.objects.filter(department=d.department,ro_lock=True).order_by('-ro_month')
			dtr = Data_Rush_Order.objects.filter(header_rush_order_id__department=d.department,
					header_rush_order_id__ro_lock=True).order_by('-header_rush_order_id__ro_month')
		
		if id == '2':
			try:
				s = request.POST['com_sort']
				if request.POST['keyword']=='Pencarian Kode Bulan' or request.POST['keyword']=='':
					key = ''
				else:
					key = request.POST['keyword']
			except:
				key = request.session['key']
				s = request.session['s']
			request.session['key'] = key
			request.session['s'] = s
			enter = True
			if s == 'Terbaru':
				data = Header_Rush_Order.objects.filter(department=d.department, requestlock=True, ro_month__contains=key).order_by('-ro_month')
			else: data = Header_Rush_Order.objects.filter(department=d.department, ro_lock=True, ro_month__contains=key).order_by('ro_month')
			dtr = Data_Rush_Order.objects.filter(header_rush_order_id__department=d.department,header_rush_order_id__ro_lock=True).order_by('-header_rush_order_id__ro_month')
		
		if id == '3':
			try:
				s2 = request.POST['com_sort2']
				if request.POST['keyword2']=='Pencarian nama barang' or request.POST['keyword2']=='':
					key2 = ''
				else:
					key2 = request.POST['keyword2']
			except:
				key2 = request.session['key2']
				s2 = request.session['s2']
			request.session['key2'] = key2
			request.session['s2'] = s2
			enter2 = True
			if s2 == 'Terbaru':
				dtr = Data_Rush_Order.objects.filter(header_rush_order_id__department=d.department,header_rush_order_id__ro_lock=True,
						ro_goods_name__contains=key).order_by('-header_rush_order_id__ro_month')
			else: dtr = Data_Rush_Order.objects.filter(header_rush_order_id__department=d.department,header_rush_order_id__ro_lock=True,
						ro_goods_name__contains=key).order_by('header_rush_order_id__ro_month')
			data = Header_Rush_Order.objects.filter(department=d.department,ro_lock=True).order_by('-ro_month')
		
		all = Data_Rush_Order.objects.filter(header_rush_order_id__department=d.department,
				header_rush_order_id__ro_lock=True).order_by('-header_rush_order_id__ro_month')
		
		nama = ['','']
		jml = list = []
		"""
		for alls in all:
			for i in range(len(nama)):
				if [alls.ro_goods_name] == [nama[i]]:
					nama[i+1] = str((int(nama[i+1]) + 1))
					break;
				else:
					if i == len(nama)-1:
						nama += [alls.ro_goods_name]
						nama += '1'	
		list.append(dict(zip(nama, jml)))
		"""
		
		for alls in all:
			jml += [alls.ro_goods_name]
		
		list = Counter(jml).most_common()
		
		
		paginator = Paginator(data, 20)
		page = request.GET.get('page')
		try:
			rkb = paginator.page(page)
		except PageNotAnInteger:
			rkb = paginator.page(1)
		except EmptyPage:
			rkb = paginator.page(paginator.num_pages)
		
		paginator2 = Paginator(dtr, 20)
		page2 = request.GET.get('page_all')
		try:
			dr = paginator2.page(page2)
		except PageNotAnInteger:
			dr = paginator2.page(1)
		except EmptyPage:
			dr = paginator2.page(paginator2.num_pages)
		
		paginator3 = Paginator(list, 20)
		page3 = request.GET.get('page_count')
		try:
			lst = paginator3.page(page3)
		except PageNotAnInteger:
			lst = paginator3.page(1)
		except EmptyPage:
			lst = paginator3.page(paginator3.num_pages)
		return render(request, 'templatesproc/internal/list_ro.html',{'hist_of':hist_of,'rkb':rkb,'key':key,'s':s,'enter':enter,'uname':uname,
						'dr':dr,'key2':key2,'s2':s2,'enter2':enter2,'list':list,'all':all,'nama':nama,'jml':jml,'lst':lst})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def detail_ro(request, id):
	try :
		level = request.session['level']
		uname = request.session['uname']
	except:
		level = ''
		pass
	if level == 'rkb_maker':
		hs = get_object_or_404(Header_Rush_Order,id=id)
		data = Data_Rush_Order.objects.filter(header_rush_order_id__id=id)
		total = 0
		for d in data:
			total += float(d.ro_total_price)
		return render(request, 'templatesproc/internal/detail_ro.html',{'hs':hs,'data':data,'total':total})
	else:
		return render(request, 'templatesproc/vendor/login_required.html')

def reportpp(request):
	user = Group.objects.get(user=request.user)
	if user.name == 'kabag_proc' or user.name == 'kasi_lokal' or user.name == 'kasi_impor' or user.name == 'kasi_intern':
		data = {}
		n = total = 0
		key = ''
		if request.method == 'POST':
			key = request.POST.get('keyword','')
			try:
				data = Data_Purchase_Request.objects.filter(header_purchase_request_id__request_month__startswith=request.POST.get('keyword',''))
				n = data.count()
				for d in data: total = total + float(d.request_total_price)
			except: pass
		return render_to_response('templatesproc/report/reportpp.html',{'data':data,'n':n,'key':key,'total':total}, RequestContext(request,{}),)
	else:
		return render_to_response('templatesproc/report/access_denied.html', RequestContext(request,{}),)
report = staff_member_required(reportpp)

def reportro(request):
	user = Group.objects.get(user=request.user)
	if user.name == 'kabag_proc' or user.name == 'kasi_lokal' or user.name == 'kasi_impor' or user.name == 'kasi_intern':
		data = {}
		n = total = 0
		key = ''
		if request.method == 'POST':
			key = request.POST.get('keyword','')
			try:
				data = Data_Rush_Order.objects.filter(header_rush_order_id__ro_month__startswith=request.POST.get('keyword',''))
				n = data.count()
				for d in data: total = total + float(d.ro_total_price)
			except: pass
		return render_to_response('templatesproc/report/reportro.html',{'data':data,'n':n,'key':key,'total':total}, RequestContext(request,{}),)
	else:
		return render_to_response('templatesproc/report/access_denied.html', RequestContext(request,{}),)
report = staff_member_required(reportpp)

def report_budget(request):
	user = Group.objects.get(user=request.user)
	if user.name == 'kabag_proc' or user.name == 'kasi_lokal' or user.name == 'kasi_impor' or user.name == 'kasi_intern' or request.user.is_superuser:
		total_exp = budget_value = sisa = 0
		thn = dep = ''
		msg = 'Pilih Departemen dan tahun anggaran yang ingin dilihat'
		dept = Department.objects.all()
		fiscal = Ms_Fiscal_Years.objects.all()
		klik = False
		if request.method == 'POST':
			if request.POST['year'] == 'Pilih tahun --' or request.POST['departemen'] == 'Pilih departemen --':
				msg = 'Isi form dengan benar. Pilih Departemen dan tahun anggaran yang ingin dilihat'
			else:
				thn = request.POST['year']
				dep = request.POST['departemen']
				try:
					budget = Budget.objects.get(year__Code=thn, department__department=dep)
					budget_value = budget.budget_value
				except: pass
				try:
					datapp = Data_Purchase_Request.objects.filter(header_purchase_request_id__fiscal_year__Code=thn, header_purchase_request_id__department__department=dep)
					for d in datapp: total_exp += d.request_total_price
				except: pass
				try:
					dataro = Data_Rush_Order.objects.filter(header_rush_order_id__fiscal_year__Code=thn, header_rush_order_id__department__department=dep)
					for d in dataro: total_exp += d.ro_total_price
				except: pass
				sisa = budget_value - total_exp
				klik = True
		return render_to_response('templatesproc/report/report_budget.html',{'thn':thn,'dep':dep,'dept':dept,'fiscal':fiscal,'msg':msg, 'total_exp':total_exp,'budget_value':budget_value,'sisa':sisa,'klik':klik}, RequestContext(request,{}),)
	else:
		return render_to_response('templatesproc/report/access_denied.html', RequestContext(request,{}),)
report = staff_member_required(report_budget)
