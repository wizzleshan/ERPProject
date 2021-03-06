from django.contrib import admin
from Apps.Asset.Property_asset.models import *
from django.contrib.auth.models import Group

class Loaning_status_admin(admin.ModelAdmin):
	list_display = ['loaning_status']
	search_fields = ['loaning_status']
	
admin.site.register(Loaning_status, Loaning_status_admin)
"""
class Maintenance_status_admin(admin.ModelAdmin):
	list_display = ['maintenance_status']
	search_fields = ['maintenance_status']

admin.site.register(Maintenance_status, Maintenance_status_admin)
"""
class Asset_type_admin(admin.ModelAdmin):
	list_display = ['type']
	search_fields = ['type']
	
admin.site.register(Asset_type, Asset_type_admin)

class Location_admin(admin.ModelAdmin):
	list_display = ['location_name']
	search_fields = ['location_name']
	
admin.site.register(Location, Location_admin)

class Asset_currency_admin(admin.ModelAdmin):
	list_display = ['currency_symbol','currency_name','currency_rate']
	search_fields = ['currency_symbol']
	
admin.site.register(Asset_currency, Asset_currency_admin)
"""
class Department_admin(admin.ModelAdmin):
	list_display = ['department_name']
	search_fields = ['department_name']
	
admin.site.register(Department, Department_admin)
"""
class Code_unit_admin(admin.ModelAdmin):
	list_display = ['unit_name']
	search_fields = ['unit_name']
	
admin.site.register(Code_unit, Code_unit_admin)
"""
class Section_admin(admin.ModelAdmin):
	list_display = ['section_name']
	search_fields = ['section_name']
	
admin.site.register(Section, Section_admin)
"""
"""
class Employee_admin(admin.ModelAdmin):
	list_display = ['employee_name','birthday','NIP','unit','department','section','address','city','NPWP']
	search_fields = ['employee_name','city','unit','department']
	list_per_page = 10

admin.site.register(Employee, Employee_admin)
"""	
class Vendor_admin(admin.ModelAdmin):
	list_display = ['vendor_name','vendor_type']
	search_fields = ['vendor_name','vendor_type']
	
admin.site.register(Vendor, Vendor_admin)

class Unit_of_measure_asset_admin(admin.ModelAdmin):
	list_display = ['unit_of_measure_detail']
	search_fields = ['unit_of_measure_detail']
	
admin.site.register(Unit_of_measure_asset, Unit_of_measure_asset_admin)

class Ms_customer_admin(admin.ModelAdmin):
	list_display =['username','customer_name','password','customer_address','customer_city','customer_phone','fax','email','customer_verified']
	search_fields = ['customer_name']
	list_editable = ['customer_verified',]
	
	def suit_row_attributes(self, obj, request):
		css_class = {
			True: 'info', False:'error' }.get(obj.customer_verified)
		if css_class:
			return {'class': css_class, 'data': obj.customer_verified}
	
	def get_readonly_fields(self, request, obj=None):
		data = Group.objects.get(user=request.user)
		readonly_fields = ()
		if data.name == 'staff':
				readonly_fields = ()
							
		elif data.name == 'unit':
				readonly_fields = ('customer_verified',)
		else :
				readonly_fields = ()
		
		return readonly_fields
	#readonly_fields = ('username','customer_name','password','customer_address','customer_city','customer_phone','fax','email',)
	
admin.site.register(Ms_customer, Ms_customer_admin)

class Role_user_asset_admin(admin.ModelAdmin):
	list_display = ['user','access_level','intern_occupation','intern_date_register','department']
	list_per_page = 10

admin.site.register(Role_user_asset, Role_user_asset_admin)





