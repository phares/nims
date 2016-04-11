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
from lipisha_bulk import Lipisha_bulk

api_key = "0e6e25e7cc17631a794454bff4f6e20e"
api_signature = "KAtYL0ivt8Nv0ih5tAqxH2oYv9KxergMh1SSVETtlYuu5JENb8OM4VgEUVp+e9C1S2jM84obO6Cio5h3ViQAKbAcpGM2Xt3c1xMPKFjIuOPHI6FbJLXS8pqTIPNI7pkqZw/kvETiCHL8FKH3uaS4BG7CCVQPs43lVNIPc0sYzR0="
api_environment='live'
lipisha = Lipisha(api_key, api_signature, api_environment)
lipisha.api_base_url
'https://lipisha.com/payments/accounts/index.php/v2/api'

list = {}
balance = 0
float = 'null'

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
    global list
    global balance
    global float
    data_struct_type = "records"
    #Supported file content types
    content_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     'application/vnd.ms-excel',
                     'application/vnd.oasis.opendocument.spreadsheet'
                     ]
    max_upload_size = 5242880 #5MB
    if request.user.is_authenticated():

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


                            f = lipisha.get_float(account_number="05307")
                            float = f['content']


                            for a in list:
                                fname = str(a['FirstName'])
                                lname = str(a['LastName'])
                                phone = str(a['Phone'])
                                amount = str(a['Amount'])

                                try:
                                    if (amount.isdigit() and phone.isdigit() and (100<int(amount)<70000)):
                                        total_amount +=int(amount)
                                        total_recipients +=1
                                        #a['Error'] = "error"; # Add new entry
                                    else:
                                        messages.success(request, "not int | %s | %s | %s | %s | %s |" %(fname,lname,phone,amount,e))
                                        list.remove(a)

                                except Exception as e:
                                    messages.success(request, "invalid entry | %s | %s | %s | %s | %s |" %(fname,lname,phone,amount,e))
                                    list.remove(a)




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
                                        'balance':balance,
                                        'float':float,
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

def status(request):

    global float

    if request.method == "POST":

        if request.user.is_authenticated():

            if request.user.is_staff:

                for a in list:
                    fname = str(a['FirstName'])
                    lname = str(a['LastName'])
                    phone = str(a['Phone'])
                    amount = str(a['Amount'])

                    try:
                        # send money
                        send_money = lipisha.send_money(account_number="05307", mobile_number=phone, amount=amount)
                        send_money_content = send_money['content']
                        send_money_status = send_money['status']
                        messages.success(request, send_money_status)

                    except Exception as e:
                        messages.success(request, "error")

            else:

                messages.success(request, "only staff users can execute this operation")


            data = {

                'float':float,

            }
            return render(request, 'bulk/status.html', data)
        else:
            return redirect("/accounts/login")

    else:
        return redirect("/bulk/")