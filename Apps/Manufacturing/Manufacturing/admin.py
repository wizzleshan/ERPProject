from django.contrib import admin
from Apps.Manufacturing.Manufacturing.models import *
from Apps.Manufacturing.MasterData.models import *
from Apps.Manufacturing.MasterData.models import *
from django.conf import settings

class Manufacturing_OrderAdmin(admin.ModelAdmin):
#	list_display = ['ID','Production_Request','Product','Product_Quantity','Colour_Name','Label','Category','Add_Date_Time',]
	list_display = ['ID','Production_Request','Product',]
#	list_display = ['no_reg','Product_Quantity','Colour_Name','Add_Date_Time',]
#	list_display = ['no_reg','Product_Quantity','Colour_Name','Add_Date_Time',]
	list_filter = ['Product',]
	search_filter = ['Product',]
#	list_filter = ['no_reg',]
#	search_filter = ['no_reg',]
admin.site.register(Manufacturing_Order, Manufacturing_OrderAdmin)

