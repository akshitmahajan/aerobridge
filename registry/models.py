from django.db import models
import uuid
# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.relativedelta import relativedelta
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from . import countries 
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

# Source https://stackoverflow.com/questions/63830942/how-do-i-validate-if-a-django-urlfield-is-from-a-specific-domain-or-hostname

def validate_url(value):
    if not value:
        return  # Required error is done the field
    parsed_url = urlparse(value)
    if not bool(parsed_url.scheme):
        raise ValidationError('Only urls from YouTube or SoundCloud allowed')

def two_year_expiration():
    return datetime.combine( date.today() + relativedelta(months=+24), datetime.min.time()).replace(tzinfo=timezone.utc)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null = True, blank = True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) #
    identification_number = models.CharField(max_length= 20, blank=True, null=True)
    social_security_number = models.CharField(max_length=25, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.first_name +' ' + self.last_name

    def __str__(self):
        return self.first_name +' ' + self.last_name


class Address(models.Model):
    STATE_CHOICES = (("AN",_("Andaman and Nicobar Islands")),("AP",_("Andhra Pradesh")),("AR",_("Arunachal Pradesh")),("AS",_("Assam")),("BR",_("Bihar")),("CG",_("Chandigarh")),("CH",_("Chhattisgarh")),("DN",_("Dadra and Nagar Haveli")),("DD",_("Daman and Diu")),("DL",_("Delhi")),("GA",_("Goa")),("GJ",_("Gujarat")),("HR",_("Haryana")),("HP",_("Himachal Pradesh")),("JK",_("Jammu and Kashmir")),("JH",_("Jharkhand")),("KA",_("Karnataka")),("KL",_("Kerala")),("LA",_("Ladakh")),("LD",_("Lakshadweep")),("MP",_("Madhya Pradesh")),("MH",_("Maharashtra")),("MN",_("Manipur")),("ML",_("Meghalaya")),("MZ",_("Mizoram")),("NL",_("Nagaland")),("OR",_("Odisha")),("PY",_("Puducherry")),("PB",_("Punjab")),("RJ",_("Rajasthan")),("SK",_("Sikkim")),("TN",_("Tamil Nadu")),("TS",_("Telangana")),("TR",_("Tripura")),("UP",_("Uttar Pradesh")),("UK",_("Uttarakhand")),("WB",_("West Bengal")))
                     
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_line_1 = models.CharField(max_length=140)
    address_line_2 = models.CharField(max_length=140,blank=True, null=True)
    address_line_3 = models.CharField(max_length=140,blank=True, null=True)
    postcode = models.CharField(_("post code"), max_length=10)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=2, blank=True, null=True , choices=STATE_CHOICES)
    country = models.CharField(max_length = 2, choices=countries.COUNTRY_CHOICES_ISO3166, default = 'NA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.address_line_1 

    def __str__(self):
        return self.address_line_1 


# Create your models here.
class Activity(models.Model):
    ACTIVITYTYPE_CHOICES = ((0, _('NA')),(1, _('Open')),(2, _('Specific')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    activity_type = models.IntegerField(choices=ACTIVITYTYPE_CHOICES, default = 0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.name

    def __str__(self):
        return self.name

class Authorization(models.Model):
    AREATYPE_CHOICES = ((0, _('Unpopulated')),(1, _('Sparsely Populated')),(2, _('Densely Populated')),)
    RISKCLASS_CHOICES = ((0, _('NA')),(1, _('SAIL 1')),(2, _('SAIL 2')),(3, _('SAIL 3')),(4, _('SAIL 4')),(5, _('SAIL 5')),(6, _('SAIL 6')),)
    AUTHTYPE_CHOICES = ((0, _('NA')),(1, _('Light UAS Operator Certificate')),(2, _('Standard Scenario Authorization')),)
    AIRSPACE_CHOICES = ((0, _('NA')),(1, _('Green')),(2, _('Amber')),(3, _('Red')),)
    ALTITUDE_SYSTEM = ((0, _('wgs84')),(1, _('amsl')),(2, _('agl')),(3, _('sps')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=140)
    operation_max_height = models.IntegerField(default = 0)
    operation_altitude_system = models.IntegerField(default =0, choices = ALTITUDE_SYSTEM)
    airspace_type = models.IntegerField(choices = AIRSPACE_CHOICES, default =0)
    permit_to_fly_above_crowd = models.BooleanField(default = 0)
    operation_area_type = models.IntegerField(choices=AREATYPE_CHOICES, default = 0)
    risk_type = models.IntegerField(choices= RISKCLASS_CHOICES, default =0)
    authorization_type = models.IntegerField(choices= AUTHTYPE_CHOICES, default =0)
    end_date = models.DateTimeField(default = two_year_expiration)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.title

    def __str__(self):
        return self.title

class Operator(models.Model):    
    OPTYPE_CHOICES = ((0, _('NA')),(1, _('LUC')),(2, _('Non-LUC')),(3, _('AUTH')),(4, _('DEC')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=280)
    website = models.URLField()
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) #        
    expiration = models.DateTimeField(default = two_year_expiration)
    operator_type = models.IntegerField(choices=OPTYPE_CHOICES, default = 0)
    address = models.ForeignKey(Address, models.CASCADE)
    operational_authorizations = models.ManyToManyField(Authorization, related_name = 'operational_authorizations')
    authorized_activities = models.ManyToManyField(Activity, related_name = 'authorized_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vat_number = models.CharField(max_length=25, blank=True, null=True)
    insurance_number = models.CharField(max_length=25, blank=True, null=True)
    company_number = models.CharField(max_length=25, default='CO-212')
    country = models.CharField(max_length = 2, choices=countries.COUNTRY_CHOICES_ISO3166, default = 'NA')
    
    def get_address(self):
        full_address = '%s, %s, %s, %s %s, %s' % (self.address.address_line_1, self.address.address_line_2,self.address.address_line_3,self.address.city, self.address.state, self.address.country)
        return full_address
       
    def __unicode__(self):
       return self.company_name

    def __str__(self):
        return self.company_name

class Contact(models.Model):
    ROLE_CHOICES = ((0, _('Other')),(1, _('Responsible')))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE, related_name='person_contact')    
    person = models.ForeignKey(Person, models.CASCADE)
    address = models.ForeignKey(Address, models.CASCADE)
    role_type = models.IntegerField(choices=ROLE_CHOICES, default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name

    def __str__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name


class Test(models.Model):
    TESTTYPE_CHOICES = ((0, _('Remote pilot online theoretical competency')),(1, _('Certificate of remote pilot competency')),(2, _('Other')),)
    TAKEN_AT_CHOICES = ((0, _('Online Test')),(1, _('In Authorized Test Center')),(2, _('Other')),)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_type = models.IntegerField(choices = TESTTYPE_CHOICES, default =0)
    taken_at = models.IntegerField(choices = TAKEN_AT_CHOICES, default =0)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def __unicode__(self):
       return self.name

class Pilot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE)    
    person = models.OneToOneField(Person, models.CASCADE)
    photo = models.URLField(blank=True, null=True)
    photo_small = models.URLField(blank=True, null=True)
    address = models.ForeignKey(Address, models.CASCADE)
    identification_photo = models.URLField(default='https://github.com/openskies-sh/aerobridge/blob/master/sample-data/id-card-sample.jpeg',validators=[validate_url,])
    identification_photo_small = models.URLField(default='https://github.com/openskies-sh/aerobridge/blob/master/sample-data/id-card-sample.jpeg',validators=[validate_url,])
    tests = models.ManyToManyField(Test, through ='TestValidity')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default =0)

    def __unicode__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name

    def __str__(self):
       return self.person.first_name + ' ' + self.person.last_name + ' : '+ self.operator.company_name


class TestValidity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, models.CASCADE)
    pilot = models.ForeignKey(Pilot, models.CASCADE)
    taken_at = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)

class TypeCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_certificate_id = models.CharField(max_length = 280)
    type_certificate_issuing_country = models.CharField(max_length = 280)
    type_certificate_holder = models.CharField(max_length = 140)
    type_certificate_holder_country = models.CharField(max_length = 140)
    
    def __unicode__(self):
       return self.type_certificate_holder

    def __str__(self):
       return self.type_certificate_holder


class Manufacturer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length = 140, default = 'NA')
    common_name = models.CharField(max_length = 140, default = 'NA')
    address = models.ForeignKey(Address, models.CASCADE, blank= True, null=True)
    acronym = models.CharField(max_length =10, default = 'NA')
    role = models.CharField(max_length = 140, default = 'NA', help_text="e.g. Reseller, distributor, OEM etc.")
    country = models.CharField(max_length =3, default = 'NA')
    digital_sky_id = models.CharField(max_length=140, help_text="Use the Digital Sky portal to create a Manufacturer profile and get an ID, paste it here")

    cin_document = models.URLField(help_text ='Link to certificate of Incorporation issued by ROC, MCA', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf')
    gst_document = models.URLField(help_text='Link to GST certification document', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    pan_card_document = models.URLField(help_text='URL of Manufacturers PAN Card scan', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    security_clearance_document = models.URLField(help_text='Link to Security Clearance from Ministry of Home Affairs', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    eta_document = models.URLField(help_text='Link to Equipment Type Approval (ETA) from WPC Wing', default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
       return self.common_name

    def __str__(self):
       return self.common_name

class Engine(models.Model):

    power = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    count = models.IntegerField(default =1 )
    engine_type = models.CharField(max_length=15, help_text="Specify the type of engine")
    propellor = models.CharField(max_length=140, help_text="Specify number of propellors")
    
    def __unicode__(self):
       return self.engine_type 

    def __str__(self):
       return self.engine_type 
  
class Firmware(models.Model):
    ''' A model for custom firmware '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    binary_file_url= models.URLField(help_text="Enter a url from where the firmware can be downloaded")
    public_key = models.TextField(help_text="Enter a SHA / Digest or public key to test used to secure the firmware")
    version = models.CharField(max_length=25)  
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    friendly_name = models.CharField(max_length=140, help_text="Give it a friendly name e.g. May-2021 1.2 release")
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
       return self.version

    def __str__(self):
        return self.version 
    
  
  
class Aircraft(models.Model):
    AIRCRAFT_CATEGORY = ((0, _('Other')),(1, _('FIXED WING')),(2, _('ROTORCRAFT')),(3, _('LIGHTER-THAN-AIR')),(4, _('HYBRID LIFT')),(5, _('MICRO')),(6, _('SMALL')),(7, _('MEIDUM')),(8, _('Large')),)
    AIRCRAFT_SUB_CATEGORY = ((0, _('Other')),(1, _('AIRPLANE')),(2, _('NONPOWERED GLIDER')),(3, _('POWERED GLIDER')),(4, _('HELICOPTER')),(5, _('GYROPLANE')),(6, _('BALLOON')),(6, _('AIRSHIP')),(7, _('UAV')),(8, _('Multirotor')),(9, _('Hybrid')),)
    STATUS_CHOICES = ((0, _('Inactive')),(1, _('Active')),)
  
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    operator = models.ForeignKey(Operator, models.CASCADE)
    mass = models.IntegerField()
    is_airworthy = models.BooleanField(default = 0)    
    make = models.CharField(max_length = 280, blank= True, null=True)    
    master_series = models.CharField(max_length = 280, blank= True, null=True)    
    series = models.CharField(max_length = 280, blank= True, null=True)
    popular_name = models.CharField(max_length = 280, blank= True, null=True)    
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    category = models.IntegerField(choices=AIRCRAFT_CATEGORY, default = 0)
    registration_mark = models.CharField(max_length= 10, blank= True, null=True)
    sub_category = models.IntegerField(choices=AIRCRAFT_SUB_CATEGORY, default = 7)
    icao_aircraft_type_designator = models.CharField(max_length =4, default = '0000')
    max_certified_takeoff_weight = models.DecimalField(decimal_places = 3, max_digits=10, default = 0.00)
    max_height_attainable =  models.DecimalField(decimal_places = 3, max_digits=10, default = 0.00)
    compatible_payload = models.CharField(max_length=20, blank=True, null=True) 
    commission_date = models.DateTimeField(blank= True, null= True)
    type_certificate = models.ForeignKey(TypeCertificate, models.CASCADE, blank= True, null= True)
    model = models.CharField(max_length = 280)
    esn = models.CharField(max_length = 48, default='000000000000000000000000000000000000000000000000')
    digital_sky_uin_number = models.CharField(max_length=140, help_text="Get a UIN number for this aircraft using the Digital Sky Portal")
    maci_number = models.CharField(max_length = 200)
    flight_controller_number = models.CharField(help_text= "This is the Drone ID from the RFM",max_length=140,default=0)
    controller_public_key = models.TextField(help_text= "This is the public key of the RFM used to sign log files", default=0)
    operating_frequency = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    status = models.IntegerField(choices=STATUS_CHOICES, default = 1)
    photo = models.URLField(blank=True, null=True)
    photo_small = models.URLField(blank=True, null=True)
    identification_photo = models.URLField(blank=True, null=True)
    identification_photo_small = models.URLField(blank=True, null=True)
    engine = models.ForeignKey(Engine, models.CASCADE,blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    fuel_capacity = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    max_endurance = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    max_range = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    max_speed = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    dimension_length = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00) 
    dimension_breadth = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    dimension_height = models.DecimalField(decimal_places = 2, max_digits=10, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manufactured_at = models.DateTimeField(null=True)    
    dot_permission_document = models.URLField(help_text="Link to Purchased RPA has ETA from WPC Wing, DoT for operating in the de-licensed frequency band(s). Such approval shall be valid for a particular make and model", default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])
    operataions_manual_document = models.URLField(help_text="Link to Operation Manual Document", default='https://raw.githubusercontent.com/openskies-sh/aerobridge/master/sample-data/Aerobridge-placeholder-document.pdf',validators=[validate_url])

    
    history = HistoricalRecords()

    def __unicode__(self):
        return self.operator.company_name +' ' + self.model

    def __str__(self):
        return self.operator.company_name +' ' + self.model
