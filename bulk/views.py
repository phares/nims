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
    content_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    max_upload_size = 5242880 #5MB
    if request.user.is_authenticated():
        list = {}
        name = []
        size = []
        content_type = []
        charset = []
        total_amount = 0
        total_recipients = 0


        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filehandle = request.FILES['file']
                if data_struct_type == "records":
                    list= filehandle.get_records()
                    name = filehandle.name
                    size = filehandle.size
                    content_type = filehandle.content_type
                    charset = filehandle.charset

                    if content_type in content_types:
                        if size > max_upload_size:
                            return HttpResponseBadRequest('file size too big, maintain below 5 mbs')

                        #Generator
                        ta = ( item['Amount'] for item in list )

                        for a in ta:
                            total_amount +=a
                            total_recipients +=1

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
                        return HttpResponseBadRequest('wrong content type file uploaded')
                else:
                    return HttpResponseBadRequest()
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

