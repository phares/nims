from django.shortcuts import render, get_object_or_404, redirect
from bulk.models import Transactions
from .forms import PostForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pyexcel.ext.ods3
import lipisha
from lipisha import Lipisha
import re

global list
global a
global b
global c

# Create your views here.
class UploadFileForm(forms.Form):
    file = forms.FileField()

def landing(request):

    return render(request, 'landing.html')

#Uploading file

"""
                2.5MB - 2621440
                5MB - 5242880
                10MB - 10485760
                20MB - 20971520
                50MB - 5242880
                100MB 104857600
                250MB - 214958080
                500MB - 429916160
"""

def upload(request):
    data_struct_type = "records"
    #Supported file content types
    content_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     'application/vnd.ms-excel',
                     'application/vnd.oasis.opendocument.spreadsheet'
                     ]
    max_upload_size = 5242880 #5MB
    if request.user.is_authenticated():
        list = {}
        name = []
        size = []
        content_type = []
        charset = []
        total_amount = 0
        total_recipients = 0

        #check if the form action is post then proceed else display the upload form page
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            #check if the form is valid
            if form.is_valid():
                filehandle = request.FILES['file']
                content_type = filehandle.content_type
                size = filehandle.size
                #check the size of file uploaded if it is equal to or less than the given size proceed else returns Http bad request message
                if size > max_upload_size:
                     return HttpResponseBadRequest('file size too big, maintain below 5 mbs')
                if form.is_valid() and content_type in content_types:
                    try:

                        list= filehandle.get_records()
                        name = filehandle.name
                        charset = filehandle.charset
                        rule = re.compile(r'^(?:\254)?[0|7]\d{9,13}$')

                        if data_struct_type == "records":
                            for k in list:
                                if not (k.has_key('Phone') and k.has_key('Amount') and k.has_key('FirstName') and k.has_key('LastName')):
                                    messages.success(request, "File does not contain all required heading fields | FirstName | LastName | Phone | Amount | ")
                                    form = UploadFileForm()
                                    return render_to_response(
                                        'bulk/upload.html',
                                        {
                                            'form': form,
                                            'content_type':content_type,
                                        },
                                        context_instance=RequestContext(request))


                            #Generator
                            #try:
                             #   ta = ( item['Amount'] for item in list ) #Get amount from list
                              #  vp = ( item['Phone'] for item in list ) #Get Phone number from list
                            #except Exception as e:
                             #   messages.success(request, "amount record not found %s" %(ta,e))
                              #  messages.success(request, "phone record not found %s" %(vp,e))


                            #for p in vp:
                             #      if not rule.search(str(p)):
                              #         messages.success(request, "invalid entries %s" %(p))

                            for a in list:
                                try:
                                    fname = a['FirstName']
                                    lname = a['LastName']
                                    phone = a['Phone']
                                    amount = a['Amount']
                                    total_amount +=amount
                                    total_recipients +=1
                                except Exception as e:
                                    messages.success(request, "invalid entry | %s | %s | %s | %s | %s |" %(fname,lname,phone,amount,e))


                            return render_to_response(
                                    'bulk/review.html',
                                    {
                                        'form': form,
                                        'list':list,
                                        'name':name,
                                        'size':size,
                                        'content_type':content_type,
                                        'charset':charset,
                                        'total':total_amount,
                                        'recipients':total_recipients,
                                    },
                                context_instance=RequestContext(request))

                        else:
                            return HttpResponseBadRequest("error")
                    except Exception as e:
                        print e #Need to display a message to the user about this exception
                        #messages.success(request, "Err! None supported file type uploaded")
                        messages.success(request, "Sorry an error occured %s" %e)
                else:
                    messages.success(request, "Wrong file format uploaded")

            #end of check if form.is_valid()

        #display this form if the form action is not post
        else:
            form = UploadFileForm()
        return render_to_response(
            'bulk/upload.html',
            {
                'form': form,
                'list':list,
                'name':name,
                'size':size,
                'content_type':content_type,
                'charset':charset,
            },
            context_instance=RequestContext(request))
    else:
        return redirect("/accounts/login")

#Handling the uploaded file
def handle_uploaded_file(f):
    with open('/home/isp/workspace/nims/name.odt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def review(request):
    if request.user.is_authenticated():

        return render(request, 'bulk/review.html')
    else:
        return redirect("/accounts/login")

def status(request):
    if request.user.is_authenticated():

        mydata = Transactions.objects.all()
        data = {'mydata': mydata}
        return render(request, 'bulk/status.html', data)
    else:
        return redirect("/accounts/login")

def test(request, id=None):

    if request.user.is_authenticated():

        #instance = Transactions.objects.get(id=1)
        queryset = Transactions.objects.all()
        context = {
            "queryset":queryset,
            "title":"This user is authenticated"
        }
    else:

        context = {
            "title":"Sign in first"
        }

    return render(request, 'bulk/test.html', context)

def test_detail(request, id=None):

    if request.user.is_authenticated():

        #instance = Transactions.objects.get(id=1)
        instance = get_object_or_404(Transactions, id=id)
        context = {
            "instance" : instance,
            "title":"This user is authenticated"
        }
    else:

        context = {
            "title":"Sign in first"
        }

    return render(request, 'bulk/detail.html', context)

def create(request):
    form = PostForm(request.POST or None )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")

    else:
        messages.success(request, "Not Successfully created")
    context = {
        "form":form,
    }
    return render(request, 'bulk/form.html', context)

def update(request ,id=None):

    instance = get_object_or_404(Transactions, id=id)
    form = PostForm(request.POST or None, instance=instance )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Successfully updated")

        #return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "form":form,
    }
    return render(request, 'bulk/form.html', context)

def delete(request ,id=None):

    instance = get_object_or_404(Transactions, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("bulk:test")



def lipisha_(request):

    try:

        api_key = "54e2ffe282f3bdf63e20bcd2977b5ad9"
        api_signature = "alJC5xPr7bmDgNjdiCtwZMjwUiDwevQIGdXs37tDmOSgLrihbTYY5kBn8hJC9lYg8Xa1mu8U7NPWb2x61mG1Ifbp0wYyBJZ0kpKK1WYtXMBHrZq2daY7nlWnTHIx5SSU1phSTuCogTovk19OoffUVjN92nlkLmlV4qcb5+kcJF0="
        lipisha = Lipisha(api_key, api_signature, api_environment='test')
        lipisha.api_base_url
        'http://lipisha.com/index.php/v2/api/'

        #Get Balance
        c = lipisha.get_balance()

        content = c['content']
        status = c['status']

        #get float
        float = lipisha.get_float(account_number="01260")
        float_content = float['content']
        float_status = float['status']

        #confirm transaction
        confirm = lipisha.confirm_transaction(transaction='4V8KPI7JM')
        confirm_content = confirm['content']
        confirm_status = confirm['status']

        #create account
        create_account = lipisha.create_payment_account(transaction_account_type=1,
                                   transaction_account_name="MPESA Payments",
                                   transaction_account_manager="xxxx")

        create_content = create_account['content']
        create_status = create_account['status']

        #get transactions
        get_transactions = lipisha.get_transactions()

        get_content = get_transactions['content']
        get_status = get_transactions['status']

        #get customers
        customers = lipisha.get_customers()

        customers_content = customers['content']
        customers_status = customers['status']

        #get a given customer
        customer = lipisha.get_customers(customer_mobile_number="")

        customer_content = customer['content']
        customer_status = customer['status']

        #send airtime
        send_airtime = lipisha.send_airtime(account_number="01261", mobile_number="0790331936", amount="10", network="SAF")

        send_airtime_content = send_airtime['content']
        send_airtime_status = send_airtime['status']

        #send money
        send_money = lipisha.send_money(account_number="01260", mobile_number="0790331936", amount=50)

        send_money_content = send_money['content']
        send_money_status = send_money['status']

        #authorize card transaction
        authorize_card_transaction = lipisha.authorize_card_transaction(account_number="012601",
                                       card_number="4242424242424242",
                                       address1="PO BOX 11111 99999",
                                       address2="",
                                       expiry="082020",
                                       name="Lipsha Test Account",
                                       country="KENYA",
                                       state="NAIROBI",
                                       zip="00200",
                                       security_code="999",
                                       amount=100,
                                       currency='KES')

        authorize_card_transaction_content = authorize_card_transaction['content']
        authorize_card_transaction_status = authorize_card_transaction['status']

        #withdrawal account
        create_withdrawal_account = lipisha.create_withdrawal_account(transaction_account_type="1",
                               transaction_account_name="Settlement Bank A/C",
                               transaction_account_number="0100555555555",
                               transaction_account_bank_name="AZY Bank",
                               transaction_account_bank_branch="HQ",
                               transaction_account_bank_address="PO BOX 900032 - 99999 Nairobi, Kenya",
                               transaction_account_swift_code="ABCXYXXXX",
                               transaction_account_manager="nimso")

        create_withdrawal_account_content = create_withdrawal_account['content']
        create_withdrawal_account_status = create_withdrawal_account['status']

        return render_to_response(
        'bulk/lipisha.html',
        {
            'content':content,
            'status':status,

            'float_content':float_content,
            'float_status':float_status,

            'confirm_content':confirm_content,
            'confirm_status':confirm_status,

            'create_content':create_content,
            'create_status':create_status,

            'get_content':get_content,
            'get_status':get_status,

            'get_transactions':get_transactions,
            'create_account':create_account,

            'customers_content':customers_content,
            'customers_status':customers_status,

            'customer_content':customer_content,
            'customer_status':customer_status,

            'send_airtime_content':send_airtime_content,
            'send_airtime_status':send_airtime_status,

            'send_money_content':send_money_content,
            'send_money_status':send_money_status,

            'authorize_card_transaction_content':authorize_card_transaction_content,
            'authorize_card_transaction_status':authorize_card_transaction_status,

            'create_withdrawal_account_content':create_withdrawal_account_content,
            'create_withdrawal_account_status':create_withdrawal_account_status,
        },
        context_instance=RequestContext(request))
    except Exception as e:
        messages.success(request, "Sorry an error occured %s" %e)
        return render_to_response(
            'bulk/upload.html',
            {


            },
            context_instance=RequestContext(request))