from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from.models import  *
from datetime import date
from django.db.models import Q


def index(request):
    return render(request,'index.html')

def registration(request):
    return render(request,'registration.html')

def admin_login(request):
    error =""
    if request.method =='POST':
        u=request.POST['username']
        p=request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    return render(request,'admin_login.html',locals())

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    totalservices =Services.objects.all().count
    totalunread = Contact.objects.filter(isread="no").count
    totalread = Contact.objects.filter(isread="yes").count
    totalnewbooking = SiteUser.objects.filter(status=None).count
    totaloldbooking = SiteUser.objects.filter(status="1").count
    return render(request,'admin_home.html',locals())

def Logout(request):
    logout(request)
    return redirect(index)

def add_services(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=" "
    if request.method=="POST":
        st=request.POST['servicetitle']
        des = request.POST['description']
        image = request.FILES['image']
        try:
            Services.objects.create(title=st,description=des,image=image)
            error="no"
        except:
            error = "yes"
    return render(request,'add_services.html',locals())


def manage_services(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    services= Services.objects.all()
    return render(request,'manage_services.html',locals())

def edit_services(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    service=Services.objects.get(id=pid)
    error=" "
    if request.method=="POST":
        st=request.POST['servicetitle']
        des = request.POST['description']

        service.title = st
        service.description = des

        try:
            service.save()
            error="no"
        except:
            error="yes"

        try:
            image = request.FILES['image']
            service.image = image
            service.save()
        except:
            pass



    return render(request,'edit_services.html',locals())

def delete_services(request,pid):
    service =Services.objects.get(id=pid )
    service.delete()
    return redirect('manage_services')


def services(request):

    services= Services.objects.all()
    return render(request,'services.html',locals())

def about(request):


    return render(request,'about.html')


def request_quote(request):

    error=" "
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        location = request.POST['location']
        shiftingloc = request.POST['shiftingloc']
        shiftingdate = request.POST['shiftingdate']
        briefitems = request.POST['briefitems']
        items = request.POST['items']

        try:
            SiteUser.objects.create(name=name,email=email,mobile=contact,location=location,shiftingloc=shiftingloc,shiftingdate=shiftingdate,briefitems=briefitems,items=items,requestdate=date.today())
            error="no"
        except:
            error = "yes"
    return render(request,'request_quote.html',locals())

def new_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking= SiteUser.objects.filter(status=None)
    return render(request,'new_booking.html',locals())

def view_bookingdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking= SiteUser.objects.get(id=pid)
    if request.method=="POST":
        remark = request.POST['remark']
        try:
            booking.remark = remark
            booking.status = "1"
            booking.updationdate = date.today()
            booking.save()
            error = "no"

        except:
            error = "yes"

    return render(request,'view_bookingdetail.html',locals())


def old_booking(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    booking= SiteUser.objects.filter(status="1")
    return render(request,'old_booking.html',locals())

def delete_booking(request,pid):
    booking =SiteUser.objects.get(id=pid )
    booking.delete()
    return redirect('old_booking')

def contact(request):
    error="no"
    if request.method == 'POST':
        n = request.POST['fullname']
        c = request.POST['contact']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n,contact=c,emailid=e,subject=s,message=m,mdate=date.today(),isread="no")
            error="no"
        except:
            error ="yes"
    return render(request,'contact.html',locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact= Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html',locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact= Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html',locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact= Contact.objects.get(id=pid)
    contact.isread="yes"
    contact.save()
    return render(request,'view_queries.html',locals())

def delete_query(request,pid):
    contact =Contact.objects.get(id=pid )
    contact.delete()
    return redirect('read_queries')

def search(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sd = None

    if request.method == 'POST':
        sd = request.POST['searchdata']

    try:
        booking = SiteUser.objects.filter(Q(name=sd) |Q(mobile=sd))

    except:
        booking = ""

    print(booking)
    return render(request,'search.html',locals())


def betweendate_bookingreport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sd = None

    if request.method == 'POST':
        fd = request.POST['fromdate']
        td = request.POST['todate']
        booking= SiteUser.objects.filter(Q(requestdate__gte=fd)& Q(requestdate__lte=td))
        return render(request,'bookingbtwdates.html',locals())


    return render(request,'betweendate_bookingreport.html',locals())

def betweendate_contactreport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sd = None

    if request.method == 'POST':
        fd = request.POST['fromdate']
        td = request.POST['todate']
        contact= Contact.objects.filter(Q(mdate__gte=fd)& Q(mdate__lte=td))
        return render(request,'contactbtwdates.html',locals())


    return render(request,'betweendate_contactreport.html',locals())
