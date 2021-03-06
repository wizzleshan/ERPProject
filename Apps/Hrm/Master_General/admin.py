''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Master_General.models import *
from django.utils.translation import ugettext_lazy as _


class DepartmentAdmin (admin.ModelAdmin):   
    list_display = ('department',)
    list_search = ['department',]    

admin.site.register(Department, DepartmentAdmin)


class BankAdmin (admin.ModelAdmin):
    list_display = ('name_bank','address',)    
    list_filter = ('name_bank',)
    list_search = ['name_bank']

admin.site.register (Bank, BankAdmin)    
    

class Level_PositionAdmin (admin.ModelAdmin):   
    list_display = ('level_position',)
    list_search = ['level_position',]
    
admin.site.register(Level_Position, Level_PositionAdmin)

 
class SectionAdmin (admin.ModelAdmin):
    list_display = ('section',)
    list_search = ['section',]
    
admin.site.register(Section, SectionAdmin)

   
class Master_PositionAdmin (admin.ModelAdmin):
    list_display = ('master_position',)
    list_search = ['master_position',]
    
admin.site.register(Master_Position, Master_PositionAdmin)

"""
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'rate', 'pre_symbol', 'post_symbol']
    list_filter = ['code', 'rate', 'pre_symbol', 'post_symbol']
    search_fields = ['name', 'code', 'rate']
    
admin.site.register(Currency, CurrencyAdmin)
"""
class Role_user_admin(admin.ModelAdmin):
    list_display = ['user','access_level','intern_date_register','department']
        
admin.site.register(Role_user, Role_user_admin)

