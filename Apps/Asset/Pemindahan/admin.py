from django.contrib import admin
from Apps.Asset.Pemindahan.models import *
from django.contrib.auth.models import Group
from Apps.Distribution.master_sales.models import *

class DataMovingInline(admin.TabularInline):
	model = Data_moving_request
	extra = 1
	max_num = 0
	can_delete = True
	readonly_fields = ('header','asset','request','description','moving_status',)
	"""
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header',)
			else :
				readonly_fields = ('header','asset','request','description','moving_status', )
		else: 
			readonly_fields = ('header','asset','request','description','moving_status',)
		
		return readonly_fields
	"""

class Moving_status_admin(admin.ModelAdmin):
	list_display = ['asset_moving']
	search_fields = ['asset_moving']

admin.site.register(Moving_status, Moving_status_admin)

class Header_moving_request_admin(admin.ModelAdmin):
	list_display = ['no_reg','from_department','to_department','moving_add_date','asset_reviewx','dept_reviewx','department_staff_aggrement']
	search_fields = ['no_reg','department','moving_add_date']
	inlines = [DataMovingInline,]
	list_filter = ['moving_add_date',]
	
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		data = Ms_asset.objects.filter(usage_status = 1)
		if user.name=='unit':
			return Header_moving_request.objects.filter(from_department=user2.employee.department)
		else :
			return Header_moving_request.objects.all()	
			
		if request.user.is_superuser:
			return Header_moving_request.objects.all()	
	
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Header_moving_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'no_reg', None)
			xx = True
			if getattr(obj, 'no_reg', None) == None:
				self.exclude = ['department_staff_review',]	

			else: 
				if getattr(obj, 'department_staff_aggrement') == True:
					self.exclude = ['department_staff_review','asset_staff_review',]
		else : 
			x = getattr(obj, 'no_reg', None)
			xx = True
			if getattr(obj, 'no_reg', None) == None:
				self.exclude = ['department_staff_review',]	

			else: 
				if getattr(obj, 'department_staff_aggrement') == True:
					self.exclude = ['department_staff_review','asset_staff_review',]
				else: 
					self.exclude = ['asset_staff_review',]
					
		return form

	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'unit':
			readonly_fields += ('no_reg','from_department','to_department','moving_add_date','asset_reviewx',)
			if getattr(obj, 'department_staff_aggrement', None) == True:
				readonly_fields += ('department_staff_aggrement','dept_reviewx',)
				
		elif data.name == 'staff':
			readonly_fields += ('dept_reviewx','department_staff_aggrement',)
			if getattr(obj,'department_staff_aggrement', None) == True:
				readonly_fields += ('from_department','to_department','asset_reviewx',)
		return readonly_fields
		
	
admin.site.register(Header_moving_request, Header_moving_request_admin)

class Data_moving_request_admin(admin.ModelAdmin):
	list_display = ['header','request','asset','moving_status']
	search_fields = ['header','asset','moving_status']
	list_filter = ['request']
		
	def queryset(self, request, obj=None):
		user = Group.objects.get(user=request.user)
		user2 = StaffPerson.objects.get(user=request.user)
		if user.name=='unit':
			return Data_moving_request.objects.filter(header__from_department=user2.employee.department)
		else :
			return Data_moving_request.objects.all()	
			
		if request.user.is_superuser:
			return Data_moving_request.objects.all()		
	
	def get_form(self, request, obj=None, **kwargs):
		data = Group.objects.get(user=request.user)
		form = super(Data_moving_request_admin, self).get_form(request, obj, **kwargs)
		if data.name == 'staff':
			x = getattr(obj, 'header', None)
			xx = True
			if getattr(obj, 'header', None) == None:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
			else:
				if getattr(obj, 'header', None) != None:
					if x.department_staff_aggrement == False:
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 4)
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department,usage_status=1)
						
						#form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
		
		else:
			readonly_fields = ('header','request','asset','moving_status',)
					
		return form
			
		"""		
			try:
				x = getattr(obj,'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service__startswith = 4)#jaga2 untuk permintaan penggantian
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
		else :
			readonly_fields = ('header','request','asset','moving_status',)
		return form

			x = getattr(obj, 'header', None)
			xx = True
			if getattr(obj, 'header', None) == None:
				form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(department_staff_aggrement=False)
			else :						
				if getattr(obj, 'header', None) != None:
					if x.department_staff_aggrement == False:
						form.base_fields['asset'].queryset = form.base_fields['asset'].queryset.filter(department=x.from_department,usage_status=1)
						form.base_fields['request'].queryset = form.base_fields['request'].queryset.filter(answer_service=5)
		"""
		
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
			if getattr(obj, 'header', None) == None:
				readonly_fields = ('request','asset','moving_status','description',)
			else :
				readonly_fields = ('header',)
			xx = False
			try:
				x = getattr(obj, 'header', None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == False:
				readonly_fields += ()
			else: 
				readonly_fields += ('request','asset','moving_status','description',)
				
		elif data.name == 'unit':
			if getattr(obj, 'header', None) != None:
				readonly_fields = ('header','request','asset','moving_status','description',)
			else :
				readonly_fields = ('header',)
				
			xx = False
			try:
				x = getattr(obj,'header',None)
				xx = x.department_staff_aggrement
			except: pass
			if xx == True:
				readonly_fields = ('header','request','asset','moving_status','description',)
			else :
				readonly_fields +=()
		
		return readonly_fields		


	"""	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
				xx = False
				try:
					x = getattr(obj,'header',None)
					xx = x.department_staff_aggrement
				except: pass
				if xx == True:
					readonly_fields += ('header','asset','request','description','moving_status',)
				else: 
					readonly_fields = ()
		else: 
			readonly_fields = ('header','asset','request','description','moving_status',)
		
		return readonly_fields
	"""	

admin.site.register(Data_moving_request, Data_moving_request_admin)
