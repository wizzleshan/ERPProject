""" Develop By - Fery Febriyan Syah """

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from library.const.province import PROVINCE
from datetime import datetime
from tinymce.models import HTMLField
from library.const.general import GENDER, RELIGION, NATIONAL, STATUS, EDU_STATUS, BLOOD, CHECK, RESULT1, RESULT2



class Candidate_New_Employe (models.Model):
    participant_no = models.CharField (max_length=50, editable=False, verbose_name="No Peserta")
    applicant_name = models.CharField (max_length=50, verbose_name="Nama Pelamar")
    birthday = models.DateField (max_length=20, verbose_name="Tanggal Lahir")
    religion = models.IntegerField (choices=RELIGION, verbose_name="Agama")
    gender = models.IntegerField (choices=GENDER, verbose_name="Jenis Kelamin")
    ktp_no = models.CharField (max_length=20, verbose_name="No KTP")
    national = models.IntegerField(choices=NATIONAL, verbose_name="Kewarganegaraan")
    province = models.IntegerField (choices=PROVINCE, verbose_name="Provinsi")
    city = models.CharField (max_length=50, verbose_name="Kota")
    address = HTMLField (max_length=50, verbose_name="Alamat", help_text=(' *)Alamat Lengkap'))
    status = models.IntegerField (choices=STATUS, verbose_name="Status", help_text=(' *)Status Perkawinan'))
    edu_status = models.IntegerField (choices=EDU_STATUS, verbose_name="Status Pendidikan", help_text=(' *)Pendidikan Terakhir'))
    weight = models.CharField (max_length=5, blank=True, verbose_name="Berat Badan", help_text=(' *)kg'))
    high = models.CharField (max_length=5, blank=True, verbose_name="Tinggi Badan", help_text=(' *)cm'))
    blood_group = models.IntegerField (choices=BLOOD, verbose_name="Golongan Darah")
    
    class Meta:
        verbose_name = _('Data Pelamar')
        verbose_name_plural = _('Data Pelamar')
        ordering = ['id']
    
    def addressx(self):
        return '%s' % self.address
    addressx.allow_tags = True
    addressx.short_description = 'Alamat'
    
    def incstring(self):
        
        try:
            data = Candidate_New_Employe.objects.all()
            jml = data.count()
        except:
            jml=0
            pass
        no = 0
        if jml == 0:
            no = 0
        else: 
            for d in data:
                split = str(d.participant_no).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring
    
    def inclen(self):
        leng = len(self.incstring())
        return leng
    
    def participan_no(self):
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
        
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'NP/%(year)s/%(month)s/%(unik)s' % {'year' : intyear,
                                                    'month' : strnow,
                                                    'unik' : number}
    def save(self, force_insert=False, force_update=False, using=None):
        if self.participant_no == '':
            self.participant_no = self.participan_no()
        else: self.participant_no = self.participant_no
        super(Candidate_New_Employe, self).save()
        

    def __unicode__(self):
        return '%s' % self.participant_no
    
class Role (models.Model):
    aplicant_name = models.ForeignKey (Candidate_New_Employe, verbose_name="Nama pelamar")
    certificate = models.IntegerField (choices=CHECK, verbose_name="Ijazah Terahir")
    transcript = models.IntegerField (choices=CHECK, verbose_name="Transkip Nilai")
    SKCK = models.IntegerField (choices=CHECK, verbose_name="SKCK")
    bill_of_health = models.IntegerField (choices=CHECK, verbose_name="Surat Sehat")
    birth_certificate = models.IntegerField (choices=CHECK, verbose_name="Akte Kelahiran")
    copy_ktp = models.IntegerField (choices=CHECK, verbose_name="Fotocopy KTP")
    
    class Meta:
        verbose_name_plural = "Persyaratan Khusus"
        
    def __unicode__(self):
        return '%s' % self.id
        
   
class Test (models.Model):
    aplicant_name = models.OneToOneField (Candidate_New_Employe, verbose_name="Nama Pelamar")
    date = models.DateField (verbose_name="Tanggal Penyeleksian")
    administrasion = models.IntegerField (verbose_name="Tes Administrasi")
    date = models.DateField (verbose_name="Tanggal Interview 1", blank=True)
    interview_1 = models.IntegerField (verbose_name="Tes Interview 1", blank=True)
    date = models.DateField (verbose_name="Tanggal Psykotest", blank=True)
    psykotest = models.IntegerField (verbose_name="Psykotest", blank=True)
    date = models.DateField (verbose_name="Tanggal Tes Kesehatan", blank=True)
    health = models.IntegerField (verbose_name="Tes Kesehatan", blank=True)
    located = models.TextField (max_length=50, verbose_name="Lokasi Penyeleksian", blank=True)
    date = models.DateField (verbose_name="Tanggal interview 2", blank=True)
    interview_2 = models.IntegerField (verbose_name="Tes Interview 2", blank=True)
    
    class Meta:
        verbose_name_plural = "Penyeleksian"
        
    def __unicode__(self):
        return '%s' % self.id   
    
class Result (models.Model):
    aplicant_name = models.OneToOneField (Candidate_New_Employe, verbose_name="Nama Pelamar")
    administrasion = models.CharField (choices=RESULT1, max_length=1, verbose_name="Tes Administrasi")
    interview_1 = models.CharField (choices=RESULT1, max_length=1, verbose_name="Tes Interview 1")
    psykotest = models.CharField (choices=RESULT1, max_length=1, verbose_name="Psykotets")
    health = models.CharField (choices=RESULT1, max_length=1, verbose_name="Tes Kesehatan")
    interview_2 = models.CharField (choices=RESULT1, max_length=1, verbose_name="Tes Interview 2")
    desicion = models.CharField (choices=RESULT2, max_length=1, verbose_name="Keputusan")
    
    class Meta:
        verbose_name_plural = "Hasil"
        
    def __unicode__(self):
        return '%s' % self.id
        
    
