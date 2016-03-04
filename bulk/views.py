from django.shortcuts import render
from bulk.models import Transactions

# Create your views here.

def index(request):

    data = {'mydata': "upload"}
    return render(request, 'bulk/index.html', data)

def review(request):

    data = {'mydata': "review"}
    return render(request, 'bulk/review.html', data)

def status(request):

    mydata = Transactions.objects.all()
    data = {'mydata': mydata}
    return render(request, 'bulk/status.html', data)

