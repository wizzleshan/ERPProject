﻿from django.db import models
from datetime import datetime
from Apps.Inventory.Inventory_Planing.models import Warehouse, Warehouse_material
from Apps.Inventory.Property_Inv.models import type_commodity, quantity_commodity, Jenis_satuan
from django.utils.translation import ugettext as _
from Apps.Manufacturing.ProductionExecution.models import production_record
from tinymce.models import HTMLField
from django.db.models.signals import post_save

class Ms_commodity (models.Model):
    warehouse_name = models.ForeignKey (Warehouse, verbose_name="Nama Gudang")
    no_commodity = models.ForeignKey (production_record, verbose_name="No Produksi")
    name_commodity = models.CharField (max_length=50, verbose_name="Nama Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_stock = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)


    class Meta:
        verbose_name_plural= _('Master Barang Produksi')
        verbose_name= _('Master Barang Produksi')


    def __unicode__(self):
        return u'%s' % self.name_commodity

def capatity(sender, instance, created, **kwargs):
    if created:
        w = Warehouse.objects.get(id=instance.warehouse_name.id)
        w.available_capacity_warehouse = w.available_capacity_warehouse - instance.total_stock
        w.save()
post_save.connect(capatity, sender=Ms_commodity)


class master_commodity (models.Model):
    warehouse_name = models.ForeignKey (Warehouse_material, verbose_name="Nama Gudang")
    commodity_name = models.CharField (max_length=50, verbose_name="Nama Barang")
    commodity_no = models.CharField (max_length=20, editable=False, verbose_name="Nomer Barang")
    quantity_commodity = models.ForeignKey (quantity_commodity, verbose_name="Kualitas Barang")
    type_commodity = models.ForeignKey (type_commodity, verbose_name="Jenis Barang")
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_stock = models.IntegerField (max_length=20, verbose_name="Jumlah Barang")
    description = HTMLField (max_length=50, verbose_name="Deskripsi",blank=True)
    #plan_month = models.CharField(max_length=6, editable=False)

    class Meta:
        verbose_name= _('Master Barang Material')
        verbose_name_plural= _('Master Barang Material')
    """
    def plan_mon (self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)

        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}

        return '%(year)s%(month)s' % {'year':intyear, 'month':strnow}
    """

    def print_pdf(self):
        img = '<img src="/media/static/staticproc/images/print.png" width="20%"/>'
        link = '<a href="/print_data_barang/%(id)s/" target="blank">%(gbr)s Cetak</a>' % {'id': self.id, 'gbr':img}
        return link
    print_pdf.allow_tags = True
    print_pdf.short_description = 'Print SO'

    def incstring(self):

        try:
            data = master_commodity.objects.all()
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.commodity_no).split('/')
                no = int(split[1])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def commodity_noo(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        if intnow == 12:
            intnow = 1
            intyear += 1
        else : intnow += 1
        strnow = str(intnow)


        if len(strnow) < 1 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'NB/%(unik)s' % {'unik' : number}

    def save(self, force_insert=False, force_update=False, using=None):
        if self.commodity_no == "":
            self.commodity_no = self.commodity_noo()
        else: self.commodity_no = self.commodity_no
        #if self.plan_month == '':
        #   self.plan_month = self.plan_mon()
        #else: self.plan_month = self.plan_month
        super(master_commodity, self).save()

    def __unicode__(self):
        return u'%(no)s | %(name)s' % { 'no':self.commodity_no,'name':self.commodity_name}

def capatity(sender, instance, created, **kwargs):
    if created:
        w = Warehouse_material.objects.get(id=instance.warehouse_name.id)
        w.available_capacity_warehouse = w.available_capacity_warehouse - instance.total_stock
        w.save()
post_save.connect(capatity, sender=master_commodity)


class handling_commodity_in (models.Model):
    commodity_name = models.ForeignKey (Ms_commodity, verbose_name="Nama Barang")
    date_in = models.DateTimeField (max_length=20, verbose_name="Tanggal Masuk", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=50, verbose_name="Jumlah Barang")
    status = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat persetujuan dari Kepala Gudang')

    class Meta:
        verbose_name_plural= _('Penanganan Barang Produksi Masuk')
        verbose_name= _('Penanganan Barang Produksi Masuk')

    def __unicode__(self):
        return u'%s' % self.id

def stocks(sender, instance, created, **kwargs):
    if instance.status == True:
        i = stock_commodity.objects.get(id=instance.commodity_name.id)
        i.total_stock = i.total_stock + instance.total_commodity
        i.save()
        n = Warehouse.objects.get(id=instance.commodity_name.warehouse_name.id)
        n.available_capacity_warehouse = n.available_capacity_warehouse - instance.total_commodity
        n.save()
post_save.connect(stocks, sender=handling_commodity_in)


class handling_commodity_out (models.Model):
    commodity_name = models.ForeignKey (Ms_commodity, verbose_name="Nama Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Keluar", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=50, verbose_name="Jumlah Barang")
    status = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat Persetujuan dari Kepala Gudang')

    class Meta:
        verbose_name_plural= _('Penanganan Barang Produksi Keluar')
        verbose_name= _('Penanganan Barang Produksi Keluar')

    def __unicode__(self):
        return u'%s' % self.id

def stock(sender, instance, created, **kwargs):
    if instance.status == True:
        o = stock_commodity.objects.get(id=instance.commodity_name.id)
        o.total_stock = o.total_stock - instance.total_commodity
        o.save()
        u = Warehouse.objects.get(id=instance.commodity_name.warehouse_name.id)
        u.available_capacity_warehouse = u.available_capacity_warehouse + instance.total_commodity
        u.save()
post_save.connect(stock, sender=handling_commodity_out)


class Mutation (models.Model):
    commodity_name = models.ForeignKey (Ms_commodity, verbose_name="Nama Barang")
    #unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    #total_commodity = models.IntegerField (max_length=50, verbose_name="Total Barang")
    warehouse_name = models.ForeignKey (Warehouse, related_name=_("Gudang Awal"), verbose_name="Gudang Awal")
    to_warehouse = models.ForeignKey (Warehouse, related_name=_("Pindah Ke Gudang"), verbose_name="Pindah Ke Gudang")
    date = models.DateTimeField (verbose_name="Terhitung Tanggal", blank=True)
    description = HTMLField (verbose_name="Deskripsi")
    agrement = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat persetujuan dari kepala Gudang')

    class Meta:
        verbose_name= _('Pemindahan Barang Produksi')
        verbose_name_plural= _('Pemindahan Barang Produksi')

    def __unicode__(self):
        return u'%s' % self.id

def moving(sender, instance, created, **kwargs):
    if instance.agrement == True:
        data = Ms_commodity.objects.get(id=instance.commodity_name.id)
        move = Ms_commodity(id=data.id, warehouse_name=instance.to_warehouse , no_commodity=data.no_commodity, name_commodity=data.name_commodity, quantity_commodity=data.quantity_commodity, unit=data.unit, total_stock=data.total_stock, description=data.description)
        move.save()

post_save.connect(moving, sender=Mutation)

class Mutation_material (models.Model):
    commodity_name = models.ForeignKey (master_commodity, verbose_name="Nama Barang")
    #unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    #total_commodity = models.IntegerField (max_length=50, verbose_name="Total Barang")
    warehouse_name = models.ForeignKey (Warehouse_material, related_name=_("Gudang Awal"), verbose_name="Gudang Awal")
    to_warehouse = models.ForeignKey (Warehouse_material, related_name=_("Pindah Ke Gudang"), verbose_name="Pindah Ke Gudang")
    date = models.DateTimeField (verbose_name="Terhitung Tanggal", blank=True)
    description = HTMLField (verbose_name="Deskripsi")
    agrement = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat persetujuan dari kepala Gudang')

    class Meta:
        verbose_name= _('Pemindahan Barang Material')
        verbose_name_plural= _('Pemindahan Barang Material')

    def __unicode__(self):
        return u'%s' % self.id

def moving(sender, instance, created, **kwargs):
    if instance.agrement == True:
        data = master_commodity.objects.get(id=instance.commodity_name.id)
        move = master_commodity(id=data.id, warehouse_name=instance.to_warehouse, commodity_name=data.commodity_name, commodity_no=data.commodity_no, quantity_commodity=data.quantity_commodity, type_commodity=data.type_commodity, unit=data.unit, total_stock=data.total_stock, description=data.description)
        move.save()

post_save.connect(moving, sender=Mutation_material)


class handling_commodity_material_in (models.Model):
    commodity_name = models.ForeignKey (master_commodity, verbose_name="Nama Barang")
    date_in = models.DateTimeField (max_length=20, verbose_name="Tanggal Masuk", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=50, verbose_name="Jumlah Barang")
    status = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat persetujuan dari Kepala Gudang')

    class Meta:
        verbose_name_plural= _('Penanganan Barang Material Masuk')
        verbose_name= _('Penanganan Barang Material Masuk')

    def __unicode__(self):
        return u'%s' % self.id

def stocks(sender, instance, created, **kwargs):
    if instance.status == True:
        i = master_commodity.objects.get(id=instance.commodity_name.id)
        i.total_stock = i.total_stock + instance.total_commodity
        i.save()
        n = Warehouse_material.objects.get(id=instance.commodity_name.warehouse_name.id)
        n.available_capacity_warehouse = n.available_capacity_warehouse - instance.total_commodity
        n.save()
post_save.connect(stocks, sender=handling_commodity_material_in)


class handling_commodity_material_out (models.Model):
    commodity_name = models.ForeignKey (master_commodity, verbose_name="Nama Barang")
    date = models.DateTimeField (max_length=20, verbose_name="Tanggal Keluar", blank=True)
    unit = models.ForeignKey (Jenis_satuan, verbose_name="Satuan Barang")
    total_commodity = models.IntegerField (max_length=50, verbose_name="Jumlah Barang")
    status = models.BooleanField (verbose_name="Di Setujui",help_text='Jangan di centang apabila masih belum dapat Persetujuan dari Kepala Gudang')

    class Meta:
        verbose_name_plural= _('Penanganan Barang Material Keluar')
        verbose_name= _('Penanganan Barang Material Keluar')

    def __unicode__(self):
        return u'%s' % self.id

def stock(sender, instance, created, **kwargs):
    if instance.status == True:
        o = master_commodity.objects.get(id=instance.commodity_name.id)
        o.total_stock = o.total_stock - instance.total_commodity
        o.save()
        u = Warehouse_material.objects.get(id=instance.commodity_name.warehouse_name.id)
        u.available_capacity_warehouse = u.available_capacity_warehouse + instance.total_commodity
        u.save()
post_save.connect(stock, sender=handling_commodity_material_out)
