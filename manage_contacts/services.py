
import datetime
from datetime import timezone
from django.utils.dateparse import parse_date


from django.contrib.auth.models import User
from .models import Contact, Organization, Product, Entitlement


# Possibly redundant mehods #
def get_model_fields(model):
    """ Return the model fields for specified model """
    return model._meta.fields

def get_model_choices(model_fields):
    """ Get model choices for form fields """
    choice_list = []
    for field in model_fields:
        choice_list.append((field.name, field.name))

    return choice_list

def get_choice_list(model_header):
    """ Get list of choices """
    choice_list = []
    for key in model_header:
        choice_list.append((key, model_header[key]))

    return choice_list


##Basic service methods
def get_superuser_id(super_username):
    """ Attempts to return the contact id for the specified username """
    try:
        super_user = User.objects.filter(username=super_username).get()
        contact_data = Contact.objects.filter(user=super_user.id).get()

        super_id = contact_data.id 
        return super_id

    except:
        return None


def get_superorg_id(super_orgname):
    """ Attempts to return the org name for the specified orgname """
    try:
        super_org = Organization.objects.filter(org_name=super_orgname).get()
        super_id = super_org.id
        return super_id

    except:
        return None


##Model object services##

def add_new_contact(user_query, contact_organization):
    """ Add new contact on user request """
    contact_username = user_query.get('username')
    password1 = user_query.get('password1')
    contact_firstname = user_query.get('contact_firstname')
    contact_lastname = user_query.get('contact_lastname')
    contact_email = user_query.get('contact_email')
    contact_role = user_query.get('contact_role')
    contact_status = user_query.get('contact_status')
    # contact_phone = user_query.get('contact_phone')

    #Create user
    user = User.objects.create_user(contact_username, contact_email, password1)
    user.first_name = contact_firstname
    user.last_name = contact_lastname
    user.save()

    #Update contact that was created on user creation
    new_contact = Contact.objects.filter(user=user).get()
    new_contact.creation_date = datetime.datetime.now()
    new_contact.role = contact_role
    new_contact.status = contact_status
    new_contact.organization = contact_organization
    new_contact.save()

    return new_contact


def delete_contact_data(current_user, contact_selection):
    """ Delete contact on user request """
    except_list = []
    super_username = 'superuser'
    super_id = get_superuser_id(super_username)

    # superadmin = User.objects.filter(username='superadmin').get()
    except_list.append(current_user.contact.id)
    except_list.append(super_id)
    try:
        for contact_id in contact_selection:
            if int(contact_id) in except_list:
                print('matched' + str(contact_id))
                pass

            else:
                contact_data = Contact.objects.filter(id=int(contact_id)).get()
                contact_data.user.delete()
                
        return True

    except:
        return contact_id


def add_new_organization(user_query):
    """ Add organization on user request """
    org_type = user_query.get('org_type')
    org_name = user_query.get('org_name')
    org_domain = user_query.get('org_domain')
    org_data = Organization.objects.all()
    org_names = []
    for org in org_data:
        org_names.append(org.org_name)

    if org_name not in org_names:
        new_org = Organization(org_type=org_type, org_name=org_name, domain=org_domain)
        new_org.save()

        success_message = "New organization created successfully"

    else: 
        success_message = "Organization exists"

    return success_message


def delete_org_data(current_user, org_selection):
    """ Delete org selection from database """
    except_list = []
    super_orgname = 'automai'
    super_id = get_superorg_id(super_orgname)
    except_list.append(super_id)
    except_list.append(current_user.contact.organization.id)
    try:
        for org_id in org_selection:
            org_data = Organization.objects.filter(id=int(org_id)).get()
            if org_data.id in except_list:
                pass
            
            else:      
                org_data.delete()
        
        return True

    except:
        return org_id


def add_new_product(user_query):
    """ Add new product on user request """
    product_name = user_query.get('product_name')
    product_version = user_query.get('product_version')
    product_data = Product.objects.all()
    product_names = []
    for product in product_data:
        product_names.append(product.product_name)

    if product_name not in product_names:
        new_product = Product(product_name=product_name, product_version=product_version)
        new_product.save()

        success_message = "New product created successfully"

    else: 
        success_message = "Product exists"

    return success_message


def delete_product_data(product_selection):
    """ Delete product selection from database """
    try:
        for product_id in product_selection:
            product_data = Product.objects.filter(id=int(product_id)).get()
            product_data.delete()
        
        return True

    except:
        return product_id


def add_new_entitlement(contact_data, user_query):
    """ Add new entitlement on user selection """
    creator_email = contact_data.user.email
    creator_phone = contact_data.phone
    
    product_choice = user_query.get('product_choice')
    org_choice = user_query.get('org_choice')
    product_object = Product.objects.filter(product_name=product_choice).get()
    org_object = Organization.objects.filter(org_name=org_choice).get()

    max_licenses = user_query.get('max_licenses')
    total_licenses = max_licenses

    host_ip = user_query.get('host_ip')
    product_grade = user_query.get("product_grade")
    product_stations = user_query.get("product_stations")

    creation_date = datetime.datetime.now()

    expiration_date = user_query.get('expiration_date')
    exp_date_strp = datetime.datetime.strptime(expiration_date, "%m/%d/%Y")
    expiration_date = exp_date_strp




    # print(creation_date)
    # print(expiration_date)

    # crt_date_utc = creation_date.replace(tzinfo=timezone.utc).timestamp()
    # exp_date_utc = expiration_date.replace(tzinfo=timezone.utc).timestamp()


    allowed_ips = user_query.get('allowed_ips')
    re_seller = user_query.get('re_seller')

    is_permanent = user_query.get('is_permanent')
    if is_permanent:
        is_permanent = True
    
    else:
        is_permanent = False

    entitlement_data = Entitlement.objects.all()
    entitlement_names = []
    for entitlement in entitlement_data:
        entitlement_names.append(entitlement.get_entitlement_name())

    dup_check = org_object.org_name + '/' + product_object.product_name
    
    if dup_check not in entitlement_names:
        new_entitlement = Entitlement(max_licenses=max_licenses, 
                                    total_licenses=total_licenses,
                                    product=product_object, 
                                    organization=org_object, 
                                    creator_email=creator_email,
                                    creator_phone=creator_phone,
                                    re_seller=re_seller,
                                    host_ip=host_ip,
                                    is_permanent=is_permanent,
                                    product_grade=product_grade,
                                    product_stations=product_stations,
                                    allowed_ips=allowed_ips,
                                    creation_date=creation_date,
                                    expiration_date=expiration_date,
        )

        new_entitlement.save()

        success_message = "New entitlement created successfully"

    else: 
        success_message = "Entitlement exists"

    return success_message


def delete_entitlement_data(entitlement_selection):
    """ Delete entitlement selection from database """
    try:
        for ent_id in entitlement_selection:
            ent_data = Entitlement.objects.filter(id=int(ent_id)).get()
            ent_data.delete()
        
        return True

    except:
        return ent_id



##JS Table Services##

def get_contact_header():
    """ Get header data for populating tables """
    contact_header = {'username':'User',
                      'first_name':'First Name',
                      'last_name':'Last Name',
                      'email':'Email',
                      'role':'Role',
                      'status':'Status',
                      'org_name':'Organization',
                    }

    return contact_header


def get_org_header():
    org_header = {"org_type":"Type",
                  "org_name":"Name",
                  "domain":"Domain",
                }

    return org_header

def get_product_header():
    product_header = {'product_name':'Product',
                      'product_version':'Version',
                        }

    return product_header

def get_entitlement_header():
    entitlement_header = {"product_name":"Product",
                          "product_version":"Version",
                          "max_licenses":"Max",
                          "total_licenses":"Total",
                          "num_allocated":"Num Allocated",
    }
    return entitlement_header



#Create table data based on header keys and object data#
## Data model must have get_table_dictionary function ##
def get_table_data(table_header, object_data):
    """ Create a data object to populate table """
    data = {}
    header_list = []
    for key in table_header.keys():
        header_list.append(table_header[key])
    data['table_header'] = header_list
    if len(object_data) > 0:
        try:
            data_list = []
            for obj in object_data:

                object_dictionary = obj.get_table_dictionary()
                temp_dict = {}
                temp_dict["data_id"] = object_dictionary.get("data_id")

                for key in table_header.keys():
                    if key in object_dictionary.keys():
                        temp_dict[key] = object_dictionary.get(key)

                data_list.append(temp_dict)

            data['table_data'] = data_list
            data['success'] = True

        except:
            data['success'] = False

    return data
