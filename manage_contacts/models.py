import datetime
from datetime import timezone

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from manage_licenses.models import License

class Organization(models.Model):
    # org_id = models.IntegerField(null=True)
    # org_id = models.CharField(max_length=7, default='0000000', editable=False)
    org_id = id
    ORG_TYPE_CHOICES = [('customer', 'customer'), ('customer', 'partner')]
    org_type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES, null=True)
    org_name = models.CharField(max_length=50, unique=True)
    domain = models.CharField(max_length=50)

    def get_table_dictionary(self):
        org_dict = {}
        org_dict["data_id"] = self.id
        org_dict["org_type"] = self.org_type
        org_dict["org_name"] = self.org_name
        org_dict["domain"] = self.domain
        return org_dict

    def __str__(self):
        return self.org_name

class Contact(models.Model):
    phone = models.IntegerField(null=True)
    creation_date = models.DateTimeField("Date Created", null=True)
    ROLE_CHOICES = [('admin', 'admin'), ('user', 'user')]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True)
    STATUS_CHOICES = [('active', 'active'), ('removed', 'removed')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True)

    def get_table_dictionary(self):
        contact_dict = {}
        contact_dict["data_id"] = self.id
        contact_dict["username"] = self.user.username
        contact_dict["first_name"] = self.user.first_name
        contact_dict["last_name"] = self.user.last_name
        contact_dict["email"] = self.user.email
        contact_dict["contact_id"] = self.id
        contact_dict["role"] = self.role
        contact_dict["status"] = self.status
        contact_dict["org_id"] = self.organization.id
        contact_dict["org_name"] = self.organization.org_name
        return contact_dict

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)
    instance.contact.save()

class Product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    product_version = models.CharField(max_length=50, null=True)

    def get_table_dictionary(self):
        product_dict = {}
        product_dict["data_id"] = self.id
        product_dict["product_name"] = self.product_name
        product_dict["product_version"] = self.product_version
        return product_dict

    def __str__(self):
        return self.product_name

class Entitlement(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    max_licenses = models.IntegerField(default=100)
    total_licenses = models.IntegerField(default=0)
    creator_email = models.CharField("Created by ", max_length=50, null=True)
    creator_phone = models.IntegerField(default=0, null=True)
    re_seller = models.CharField(max_length=50, null=True)
    host_ip = models.CharField(max_length=50, null=True)
    is_permanent = models.BooleanField(default=None, null=True)
    product_grade = models.CharField(max_length=50, default="standard", null=True)
    product_stations = models.IntegerField(default=0, null=True)
    allowed_ips = models.IntegerField(default=10, null=True)
    creation_date = models.DateTimeField("Date created ", null=True)
    expiration_date = models.DateTimeField("Expiration date ", null=True)

    def __str__(self):
        return self.organization.org_name + "/" + self.product.product_name

    def get_entitlement_name(self):
        return self.organization.org_name + "/" + self.product.product_name

    def get_table_dictionary(self):
        table_dict = {}
        table_dict["data_id"] = self.id
        table_dict["product_name"] = self.product.product_name
        table_dict["product_version"] = self.product.product_version
        table_dict["max_licenses"] = self.max_licenses
        table_dict["total_licenses"] = self.total_licenses
        num_allocated = str(self.total_licenses) + " of " + str(self.max_licenses)
        table_dict["num_allocated"] = num_allocated
        return table_dict

    def gen_license_image(self):
            new_image = License(
                organization=str(self.organization),
                product=str(self.product),
                max_licenses=str(self.max_licenses),
                total_licenses=str(self.total_licenses),
                creator_email=str(self.creator_email),
                creator_phone=str(self.creator_phone),
                re_seller=str(self.re_seller),
                host_ip=str(self.host_ip),
                is_permanent=str(self.is_permanent),
                product_grade=str(self.product_grade),
                product_stations=str(self.product_stations),
                allowed_ips=str(self.allowed_ips),
                creation_date=str(self.creation_date),
                expiration_date=str(self.expiration_date),

            )

            new_image.save()

    def get_license_header(self):
        """ Get header for displaying in license key """
        package_data = {}
        package_data["Product Name: "] = str(self.product.product_name)
        package_data["Host/IP address: "] = str(self.host_ip)
        package_data["Version: "] = str(self.product.product_version)
        package_data["Num of stations: "] = str(self.product_stations)
        package_data["Lease Start Date: "] = str(self.creation_date)
        package_data["Lease End Date: "] = str(self.expiration_date)
        package_data["Grade: "] = str(self.product_grade)
        package_data["User name: "] = str(self.creator_email)
        package_data["Support ID: "] = self.check_trial()
        package_data["Support Expiration Date: "] = str(self.expiration_date)
        return package_data

    def get_key_string(self):
        organization = self.organization.org_name
        
        task = 0
        log = 0
        node = 0
        system = 0
        snmp = 0

        creation_date = self.creation_date
        expiration_date = self.expiration_date
        crt_date_utc = creation_date.timestamp()
        exp_date_utc = expiration_date.timestamp()

        product_key = "organization=" + str(organization)
        product_key += "&product=" + self.product.product_name
        product_key += "&Ip address=" + str(self.host_ip)
        product_key += "&Hostname=" + str(self.host_ip)
        product_key += "&Version=" + str(self.product.product_version)
        product_key += "&Num of stations=" + str(self.product_stations)
        product_key += "&ips=" + str(self.allowed_ips)
        product_key += "&License Start Date=" + str(crt_date_utc)
        product_key += "&License End Date=" + str(exp_date_utc)
        product_key += "&task=" + str(task)
        product_key += "&log=" + str(log)
        product_key += "&node=" + str(node)
        product_key += "&system=" + str(system)
        product_key += "&snmp=" + str(snmp)
        product_key += "&grade=" + str(self.product_grade)
        product_key += "&sid=" + str(self.id)
        product_key += "&expdate=" + str(exp_date_utc)
        product_key += "&username=all"

        if (self.product.product_name is not "Backend" and
            self.product.product_name is not "AppLoader" and
            self.product.product_name is not "AppsWatch"):
            product_key += "&end=true"

        return product_key

    def check_trial(self):
        if self.is_permanent is True:
            return "TRIAL"

        else:
            return self.id

    def check_allocated_licenses(self):
        used_licenses = self.max_licenses - self.total_licenses
        if used_licenses < self.max_licenses:
            return True

        else:
            return False

    def subtract_license(self):
        if self.total_licenses > 0:
            self.total_licenses -= 1
            self.save()
            return True

        elif self.total_licenses == 0:
            return "no entitlements"

        else:
            return "number out of range"

    def add_license(self):
        if self.total_licenses < self.max_licenses:
            self.total_licenses += 1
            self.save()

            return True

        elif self.total_licenses == self.max_licenses:
            return "entitlements at max"

        else: 
            return "number out of range"


