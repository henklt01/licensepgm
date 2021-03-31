import datetime

import json

from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Contact, Organization, Product, Entitlement
from .forms import ContactCreationForm, SearchChoiceForm, OrgCreationForm, ProductCreationForm, EntitlementCreationForm, ChoiceForm

#Specify method imports
from .services import *


@login_required
def manage_contacts(request):
    """ Render manage-contacts html page """
    current_user = request.user
    contact_data = Contact.objects.filter(user_id=current_user.id).get()
    contact_header = get_contact_header()
    contact_choice_list = get_choice_list(contact_header)
    contact_search_form = SearchChoiceForm(auto_id='contact_search_form_%s', choice_list=contact_choice_list)

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        

    if request.method == 'POST':
        entitlement_form = EntitlementCreationForm(request.POST, product_list=product_list, org_list=org_list)
        if entitlement_form.is_valid():
            user_query = request.POST
            success_message = add_new_entitlement(contact_data, user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        print("form invalid")
        entitlement_form = EntitlementCreationForm(org_list=org_list, product_list=product_list)
    
    
    context = {'entitlement_form':entitlement_form,
            #    'contact_data':contact_data,
               'contact_search_form':contact_search_form,
            }

    return render(request, "manage_contacts/manage-contacts.html", context)

@login_required
def add_contact(request):
    """ Render add-contact html page """
    current_user = request.user
    user_id = current_user.id
    contact_data = Contact.objects.filter(user_id=user_id).get()
    contact_data = Contact.objects.filter(user_id=user_id).get()
    org_objects = Organization.objects.all()
    
    choice_list = []
    for org_object in org_objects:
        choice_list.append(org_object.org_name)

    if request.method == 'POST':
        contact_form = ContactCreationForm(request.POST)

        if contact_form.is_valid():
            user_query = request.POST
            if request.POST.get('select_org'):
                org_selection = request.POST.get('select_org')
                new_contact_org = Organization.objects.filter(org_name=org_selection).get()

            else:
                new_contact_org = contact_data.organization

            add_new_contact(user_query=user_query, contact_organization=new_contact_org)
            messages.add_message(request, messages.INFO, 'New contact created')
            return HttpResponseRedirect(request.path_info)

    else:
        contact_form = ContactCreationForm()
        contact_form.order_fields(["contact_role", "contact_status"])

    context = {'contact_data':contact_data, 'contact_form':contact_form, 'choice_list':choice_list}
    return render(request, "manage_contacts/add-contact.html", context)


def get_contact_data(request):
    """ Provide contact data for populating tables """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    org_id = user_data.organization.id
    contact_data = Contact.objects.filter(organization=org_id)
    table_header = get_contact_header()
    table_data = get_table_data(table_header, contact_data)
    return JsonResponse(table_data)


def delete_contact_selection(request, query_string):
    """ Delete contact selection on user request """
    contact_selection = json.loads(query_string)
    current_user = request.user
    response = delete_contact_data(current_user, contact_selection)
    
    if response is True:
        return get_contact_data(request)
    
    else:
        return get_contact_data(request)


## Admin Views for Automai users ##

@login_required
def admin_dash(request):
    """ Render admin dash """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name
    org_objects = Organization.objects.all()
    product_objects = Product.objects.all()
    entitlement_objects = Entitlement.objects.all()

    context = {'user_role':user_role,
               'user_org':user_org,
               'org_objects':org_objects,
               'product_objects':product_objects,
               'entitlement_objects':entitlement_objects}

    return render(request, "manage_contacts/admin-dash.html", context)


@login_required
def add_organization(request):
    """ Render add organization page"""
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        org_form = OrgCreationForm(request.POST)
        if org_form.is_valid():
            user_query = request.POST     
            success_message = add_new_organization(user_query)            
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        org_form = OrgCreationForm()


    context = {'user_role':user_role, 'user_org':user_org, 'org_form':org_form}
    return render(request, "manage_contacts/add-organization.html", context)
    

def get_org_data(request):
    """ Get org data for populating tables """
    org_data = Organization.objects.all()
    table_header = get_org_header()
    table_data = get_table_data(table_header, org_data)
    return JsonResponse(table_data)


def delete_org_selection(request, query_string):
    """ Delete org selection on user request """
    current_user = request.user
    org_selection = json.loads(query_string)
    response = delete_org_data(current_user, org_selection)
    
    if response is True:
        return get_org_data(request)
        
    else:

        return get_org_data(request)


@login_required
def add_product(request):
    """ Render add product page """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    if request.method == 'POST':
        product_form = ProductCreationForm(request.POST)
        if product_form.is_valid():
            user_query = request.POST
            success_message = add_new_product(user_query)

            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        product_form = ProductCreationForm()



    context = {'user_role':user_role, 'user_org':user_org, 'product_form':product_form}
    return render(request, "manage_contacts/add-product.html", context)
    

def get_product_data(request):
    """ Get product data for populating tables """
    product_data = Product.objects.all()
    table_header = get_product_header()
    table_data = get_table_data(table_header, product_data)
    return JsonResponse(table_data)


def delete_product_selection(request, query_string):
    """ Delete product selection on user request """
    product_selection = json.loads(query_string)
    response = delete_product_data(product_selection)
    
    if response is True:
        return get_product_data(request)
        
    else:
        return get_product_data(request)


@login_required
def add_entitlement(request):
    """ Render add entitlement page """
    current_user = request.user
    user_id = current_user.id
    user_data = Contact.objects.filter(user_id=user_id).get()
    user_role = user_data.role
    user_org = user_data.organization.org_name

    org_data = Organization.objects.all()
    org_list = []
    for organization in org_data:
        org_list.append((organization.org_name, organization.org_name))

    product_data = Product.objects.all()
    product_list = []
    for product in product_data:
        product_list.append((product.product_name, product.product_name))
        

    if request.method == 'POST':
        entitlement_form = EntitlementCreationForm(request.POST, product_list=product_list, org_list=org_list)
        if entitlement_form.is_valid():
            user_query = request.POST
            success_message = add_new_entitlement(user_query)
            messages.add_message(request, messages.INFO, success_message)
            return HttpResponseRedirect(request.path_info)

    else:
        entitlement_form = EntitlementCreationForm(org_list=org_list, product_list=product_list)
        entitlement_form.order_fields([])


    context = {'user_role':user_role, 'user_org':user_org, 'entitlement_form':entitlement_form}
    return render(request, "manage_contacts/add-entitlement.html", context)


def get_entitlement_data(request):
    """ Get entitlement data for populating tables """
    entitlement_data = Entitlement.objects.all()
    table_header = get_entitlement_header()
    table_data = get_table_data(table_header, entitlement_data)
    return JsonResponse(table_data)


def delete_entitlement_selection(request, query_string):
    """ Delete entitlement selection on user request """
    entitlement_selection = json.loads(query_string)
    response = delete_entitlement_data(entitlement_selection)
    
    if response is True:
        return get_entitlement_data(request)
        
    else:

        return get_entitlement_data(request)