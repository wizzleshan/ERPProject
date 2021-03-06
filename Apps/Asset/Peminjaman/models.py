from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.const import *
from tinymce.models import HTMLField
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Master.models import *
from Apps.Asset.Request.models import *
from datetime import datetime

class Header_loaning_request(models.Model):
	no_reg = models.CharField(verbose_name='No Reg Peminjaman', max_length=25, editable=False)
	from_department = models.ForeignKey(Department,related_name=_('Departement Asal '), max_length=25, help_text='Department Pemilik Asset yang akan Dipinjman')
	to_department = models.ForeignKey(Department, related_name=_('Departement yang Dituju '), help_text='Department yang akan Meminjam Asset')
	loan_add_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	start_loan_date = models.DateField(verbose_name=_('Tanggal Peminjaman '))
	end_loan_date = models.DateField(verbose_name=_('Tanggal Pengembalian '))
	department_staff_review = HTMLField(verbose_name=_('Review Departement Tujuan'), blank=True, null=True)
	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Departement '), default=False ,help_text='*)Jangan Disetujui dulu Sebelum Data Peminjaman Sudah Dimasukkan')
#	status = models.IntegerField(verbose_name=_('Status Peminjaman '),choices=Choice_peminjaman, default=1)
#	asset_staff_review = models.TextField(verbose_name=_('Review Asset Staff '))
#	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Asset Staff '))	
	
	
	class Meta:
		verbose_name_plural="Header Loaning Request"
		verbose_name="Header_Loaning_Request"
		
	def incstring(self):
		try:
			data = Header_loaning_request.objects.all()
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
		return 'PJ/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_loaning_request, self).save()
		
	def __unicode__(self):
		return u'%(no_reg)s | %(to_department)s' %{'no_reg':self.no_reg,'to_department':self.to_department}

class Data_loaning_request(models.Model):
	header = models.ForeignKey(Header_loaning_request, verbose_name=_('Header Loaning Request  '))
	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset '), blank=True, null=True)
	request = models.OneToOneField(Data_user_request, verbose_name=_('No. Permintaan '), blank=True, null=True)
	description = HTMLField(verbose_name=_('Deskripsi '), blank=True, null=True )	
#	no_item = models.IntegerField(verbose_name=_('No. Item'))
#	loan_amount = models.IntegerField(verbose_name=_('Jumlah Peminjaman '))
#	department_loaned = models.CharField(verbose_name=_('Depertement yang Dipinjam '), max_length=50)
	
	
	class Meta:
		verbose_name_plural="Data Loaning Request"
		verbose_name="Data_Loning_Request"
	
	def descriptionx(self):
		return '%s' % self.description
	descriptionx.allow_tags = True
	descriptionx.short_description = 'Deskripsi'
	

	def __unicode__(self):
		return '%s' % self.id
		
class Header_return_request(models.Model):
	header = models.OneToOneField(Header_loaning_request, verbose_name=_('No. Peminjaman | Peminjam '))
	return_date = models.DateField(verbose_name=_('Tanggal '), auto_now_add=True)
	asset_staff_review = HTMLField(verbose_name=_('Review Asset Staff '))
	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Pengembalian '),default=False)
#	return_month = models.DateField(verbose_name=_('Bulan '))
#	department = models.ForeignKey(Department, verbose_name=_('Nama Departement '))
#	department_staff_review = models.TextField(verbose_name=_('Review Departement '))
	
#	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Departement '))
#	department_staff_aggrement = models.BooleanField(verbose_name=_('Persetujuan Asset Staff '))	
	
	class Meta:
		verbose_name_plural="Header Return Request"
		verbose_name="Header_Return_Request"
	
	def review(self):
		return '%s' % self.asset_staff_review
	review.allow_tags = True
	review.short_description = 'Asset Staff Review'
	
		
	def __unicode__(self):
		return '%s' % self.id

#class Data_return_request(models.Model):
#	header = models.ForeignKey(Header_return_request, verbose_name=_('Header Loaning Request  '))
#	loaning = models.ForeignKey(Data_loaning_request, verbose_name=_('Data Peminjaman'))
#	status = models.ForeignKey(Loaning_status, verbose_name=_('Status Peminjaman'))
#	description = models.TextField(verbose_name=_('Deskripsi '), max_length=100)
	
#	class Meta:
#		verbose_name_plural="Data Return Request"
#		verbose_name="Data_Return_Request"
		
#		return self.header

def status_loaning(sender, instance, created, **kwargs):
	if instance.department_staff_aggrement == True:  
		data = Data_loaning_request.objects.filter(header=instance)
		for d in data:				
			aset = Ms_asset.objects.get(id=d.asset.id)
			status = Ms_asset(id=aset.id, no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, end_warranty=aset.end_warranty, location=aset.location,department=aset.department, price=aset.price, life_time=aset.life_time, salvage=aset.salvage, condition=aset.condition, add_date=aset.add_date, freq_m=aset.freq_m, status_loan=2,maintenance_status=aset.maintenance_status)
			status.save()	
						
post_save.connect(status_loaning, sender=Header_loaning_request)	

def status_return(sender, instance, created, **kwargs):
	if instance.department_staff_aggrement == True: 
		head = Header_loaning_request.objects.get(id=instance.header.id)
		data = Data_loaning_request.objects.filter(header=head)
		for d in data:				
			aset = Ms_asset.objects.get(no_reg=d.asset.no_reg)
			status = Ms_asset(id=aset.id, no_reg=aset.no_reg, asset_name=aset.asset_name, type=aset.type, end_warranty=aset.end_warranty, location=aset.location,department=aset.department, price=aset.price, life_time=aset.life_time, salvage=aset.salvage, condition=aset.condition, add_date=aset.add_date, freq_m=aset.freq_m, status_loan=1,maintenance_status=aset.maintenance_status)
			status.save()	
						
post_save.connect(status_return, sender=Header_return_request)	
