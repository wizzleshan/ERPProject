__author__ = 'FARID ILHAM Al-Q'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from PIL import Image
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField


COLOR = (('1', 'Flint'), ('2', 'Amber'), ('3', 'Green'))


class Category(models.Model):
    type = models.CharField(verbose_name=_('Kategori '), max_length=50)
    description = RichTextField(verbose_name=_('Deskripsi '), blank=True)
    image = models.ImageField(verbose_name=_('Logo '), upload_to='uploads/product', blank=True,
                              default='uploads/default.jpg')

    class Meta:
        verbose_name = 'Kategori Item'
        verbose_name_plural = 'Kategori Item'
        ordering = ['id']

    def __unicode__(self):
        return self.type

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="83"/>' % (settings.MEDIA_URL, self.image)

    display_image_description = 'Logo'
    display_image.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.image:
            return

        super(Category, self).save()
        image = Image.open(self.image)
        (width, height) = image.size
        size = (210, 217)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)


class ProductItem(models.Model):
    code_item = models.CharField(verbose_name=_('Kode Item '), unique=True, max_length=50)
    name_item = models.CharField(verbose_name=_('Nama '), max_length=50)
    color = MultiSelectField(verbose_name=_('Warna Tersedia '), max_length=50, choices=COLOR)
    category = models.ForeignKey(Category, verbose_name=_("Kategori "), blank=True)
    capacity = models.IntegerField(verbose_name=_('Kapasitas '),)
    height = models.IntegerField(verbose_name=_('Tinggi '),)
    weight = models.IntegerField(verbose_name=_('Berat '),)
    diameter = models.IntegerField(verbose_name=_('Diameter '),)
    image = models.ImageField(verbose_name=_('Gambar Botol '), upload_to='uploads/product/images', blank=True,
                              default='uploads/default.jpg', help_text='*) Gambar Botol.')
    design = models.ImageField(verbose_name=_('Design Botol '), upload_to='uploads/product/sketsa', blank=True,
                               default='uploads/default.jpg', help_text='*) Sketsa Botol.')
    description = RichTextField(verbose_name=_('Deskripsi '), blank=True)

    class Meta:
        verbose_name = _("Produk Item")
        verbose_name_plural = _("Produk Item")
        ordering = ['id']

    def __unicode__(self):
        return self.code_item

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="90"/>' % (settings.MEDIA_URL, self.image)
    display_image.short_description = 'Gambar Botol'
    display_image.allow_tags = True

    def display_color(self):
        return self.get_color_display()
    display_color.short_description = 'Warna Tersedia'

    def incstring(self):
        no = ProductItem.objects.count()
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_item(self):
        nol = 5 - self.inclen()
        if nol == 0: num = ""
        elif nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        nomor = '%(prefix)s%(unique_id)s' % {'prefix': 'Botol', 'unique_id': number}
        return nomor

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.image:
            return

        if not self.design:
            return
        image = Image.open(self.image)
        (width, height) = image.size
        size = (110, 110)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)
        design = Image.open(self.design)
        (width, height) = design.size
        size = (110, 110)
        design = design.resize(size, Image.ANTIALIAS)
        design.save(self.design.path)
        super(ProductItem, self).save()


