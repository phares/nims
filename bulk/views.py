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

# Create your views here.
class UploadFileForm(forms.Form):
    file = forms.FileField()

def landing(request):

    return render(request, 'landing.html')

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            filehandle.name
            return redirect("bulk:review")
            #return excel.make_response(filehandle.get_sheet(), "csv", file_name="download")
    else:
        form = UploadFileForm()
    return render_to_response(
        'bulk/upload.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request))


def review(request):

    data = {'mydata': "review"}
    return render(request, 'bulk/review.html', data)

def status(request):

    mydata = Transactions.objects.all()
    data = {'mydata': mydata}
    return render(request, 'bulk/status.html', data)

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

