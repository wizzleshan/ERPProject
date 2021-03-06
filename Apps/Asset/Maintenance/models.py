from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Request.models import *
from Apps.Asset.Master.models import *
from datetime import datetime

"""
class Maintenance_type(models.Model):
	maintenance_type = models.CharField(verbose_name=_('Tipe Maintenance '),max_length=35)
	description = models.TextField(verbose_name=_('Deskripsi '),blank=True)
	
	class Meta:
		verbose_name_plural="Tipe Maintenance"
		verbose_name="Tipe_Maintenance"
		
	def __unicode__(self):
		return '%s' % self.maintenance_type
"""

class Header_maintenance_asset(models.Model):
	no_reg = models.CharField(verbose_name='No Reg Maintenance', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name=_('Nama Departement '))
	rm_add_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	rm_lock = models.BooleanField(verbose_name=_('Persetujuan ?'), default=False,help_text=' )* Jangan Di Lock jika Data Maintenance Belum Dimasukkan')
	rm_lock_date = models.DateField(verbose_name=_('Batas Lock  '))
	asset_staff_review = models.TextField(verbose_name=_('Review  '), blank=True, null=True)
	maintenance_status = models.IntegerField(verbose_name=_('Status Maintenance'), choices=status_maintenance)
	finished_status = models.BooleanField(verbose_name=_('Finished Status '))

	class Meta:
		verbose_name_plural="Header Maintenance Asset"
		verbose_name= "Header_Maintenance_Asset"
		
	def incstring(self):
		try:
			data = Header_maintenance_asset.objects.all()
			jml = data.count()
		except:
			jml=0
		pass
		no = 0
		if jml == 0:
			no = 0
		else:
			for d in data:
				split = str(d.no_reg).split('/')
				no = int(split[3])
		num = no + 1
		cstring = str(num)
		return cstring
	
	def inclen(self):
		leng = len(self.incstring())
		return leng
	
	def no_rek(self):
		date = datetime.now()
		now = date.strftime("%m")
		nowyear = date.strftime("%Y")
		intnow = int(now)
		intyear = int(nowyear)
		strnow = str(intnow)
		if len(strnow) < 2 :
			strnow = '0%(strnow)s' % {'strnow' : strnow}
		nol = 5 - self.inclen()
		if nol == 1: num = "0"
		elif nol == 2: num = "00"
		elif nol == 3: num = "000"
		elif nol == 4: num = "0000"
		number = num + self.incstring()
		return 'PM/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_maintenance_asset, self).save()
		
	def __unicode__(self):
		return '%s' % self.no_reg
	
class Data_maintenance_asset(models.Model):
	header_maintenance = models.ForeignKey(Header_maintenance_asset, verbose_name=_('Header Maintenance '))
	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '), blank=True, null=True)
	user_request = models.OneToOneField(Data_user_request, verbose_name=_('No. Permintaan '), blank=True, null=True, help_text='Hanya untuk Perbaikan Mendadak')
	maintenance_type = models.IntegerField(verbose_name=_('Tipe Maintenance'), choices=tipe_maintenance, default=1)
	rm_used = models.DateField(verbose_name=_('Deadline Penggunaan '), blank=True , null=True)
	estimation = models.IntegerField(verbose_name=_('Estimasi Waktu Pemeliharaan '),blank=True, null=True, help_text='Dalam hitungan hari')
#	allocation_of_fund = models.DecimalField(verbose_name='Alokasi Dana ', max_digits=15, decimal_places=2, blank=True, null=True)
	cost_estimate = models.DecimalField(verbose_name=_('Estimasi Biaya'), max_digits=15, decimal_places=2, default=0)
	description = models.TextField(verbose_name=_('Deskripi '),blank=True)
	
	
	class Meta:
		verbose_name_plural="Data Maintenance Asset"
		verbose_name= "Data_Maintenance_Asset"
	
	def __unicode__(self):
		return '%s' % self.id
		
def maintenance_status(sender, instance, created, **kwargs):
	if instance.rm_lock == True:
		data = Data_maintenance_asset.objects.filter(header_maintenance=instance)
		for d in data:
			aset = Ms_asset.objects.get(id=d.asset.id)
			status = Ms_asset(id=aset.id, no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, end_warranty=aset.end_warranty, location=aset.location,department=aset.department, price=aset.price, life_time=aset.life_time, salvage=aset.salvage, condition=aset.condition, add_date=aset.add_date, freq_m=aset.freq_m, status_loan=aset.status_loan,maintenance_status=2)
			status.save()

post_save.connect(maintenance_status, sender=Header_maintenance_asset)
		
def finished_stat(sender, instance, created, **kwargs):
	if instance.finished_status == True:
		data = Data_maintenance_asset.objects.filter(header_maintenance=instance)
		for d in data:
			aset = Ms_asset.objects.get(id=d.asset.id)
			status = Ms_asset(id=aset.id, no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, end_warranty=aset.end_warranty, location=aset.location,department=aset.department, price=aset.price, life_time=aset.life_time, salvage=aset.salvage, condition=aset.condition, add_date=aset.add_date, freq_m=aset.freq_m, status_loan=aset.status_loan,maintenance_status=1)
			status.save()

post_save.connect(finished_stat, sender=Header_maintenance_asset)		
		
		
		
		
		
		
		
		
#class Data_maintenance_schedule(models.Model):
#	department = models.ForeignKey(Department, verbose_name=_('Nama Department '))
#	msc_date = models.DateField(verbose_name=('Tanggal Pemeliharaan '))
#	month_of_maintenance = models.DateField(verbose_name=_('Bulan Maintenance '))
#	#asset_salvage = models.ForeignKey(Asset_salvage, verbose_name=_('Nilai Residu '))
#	update_salvage = models.DecimalField(verbose_name=_('Update Nilai Residu '),decimal_places=2, max_digits=10, default=1)
#	description = models.TextField(verbose_name=_('Deskripi '), blank=True)
#	Dept_staff_review = models.TextField(verbose_name=_('Departemen Staff Review'), blank=True)	
	
#	class Meta:
#		verbose_name_plural="Data Maintenance Schedule"
#		verbose_name= "Data_Maintenance_Schedule"
	
#	def __unicode__(self):
#		return '%s' % self.id
    


