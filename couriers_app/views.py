from asyncio.windows_events import NULL
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from couriers_app.decorators import is_admin, is_depot_admin
from .models import Company, Customer, Depot, Employee, PackageDetail, TrackStatus
from couriers_app.forms import CompanyCreateDepot, CompanyCreateForm, CreatePackageForm, CustLoginForm, CustomerProfForm, CustomerRegForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def index(request):
    return render(request, 'index.html')

def track_package(request):
    if request.method == 'POST':
        trcn = request.POST['trcn']
        track_result = TrackStatus.objects.filter(track_no = trcn)
        print(track_result)
        return render(request, 'home.html', {'track_status':track_result})



@login_required(login_url='customer-login')
def cust_dashboard(request):
    return render(request, 'home.html')

@login_required(login_url='customer-login')
def cust_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='customer-login')
def cust_profile(request):
    cust = Customer.objects.get(user = request.user)
    return render(request, 'cust_profile.html', {'profile': cust, 'user': request.user})

@login_required(login_url='customer-login')
def cust_parcels(request):
    cust = Customer.objects.get(user = request.user)
    pds = PackageDetail.objects.filter(sender = cust)
    return render(request, 'cust_parcels.html',{'package':pds} )

@login_required(login_url='customer-login')
def cust_create_parcel(request):

    cust = Customer.objects.get(user = request.user)
    depot = Depot.objects.filter(zip = cust.zip)
    packForm = CreatePackageForm()

    
    str1 = datetime.now()
    ts = int(round(str1.timestamp()))
    print(ts)

    rate = 10.0

    if request.method == 'POST':
        packForm = CreatePackageForm(request.POST)
        if packForm.is_valid():
            rname = packForm.cleaned_data['r_name']
            rcontact = packForm.cleaned_data['r_contact']
            raddress = packForm.cleaned_data['r_address']
            rcity = packForm.cleaned_data['r_city']
            rzip = packForm.cleaned_data['r_zip']
            pck_det = packForm.cleaned_data['pack_details']
            pck_wt = packForm.cleaned_data['pack_weight']

            customer = Customer.objects.get(user = request.user)

            package = PackageDetail(sender = customer, r_name = rname, r_contact = rcontact, r_address = raddress, 
                                    r_city = rcity, r_zip = rzip, pick_up_depot = None, track_no = ts, pickup_datetime = None,
                                    drop_date = None, status = "Registered only", cost = 00, pack_details = pck_det, pack_weight = pck_wt )
    
            package.save()

            TrackStatus(track_no = ts, status = "Registered Only").save()

            return render(request, 'cust_sel_depot.html', {'depot' : depot, 'pck_wt' : pck_wt, 'rate' : rate, 'cost' : pck_wt * rate, 'trackn' : ts, 'pid' : package.id})
    return render(request, 'create_parcel.html', {'dep_len' : len(depot), 'form' : packForm})

@login_required(login_url='customer-login')
def final_package_booking(request):
    if request.method == 'POST':

        pid = request.POST['pid']
        did = request.POST['depot_id']
        cost = request.POST['cost']
        ts = request.POST['trcn']

        depot = Depot.objects.get(id = did)
        PackageDetail.objects.filter(id = pid).update(pick_up_depot = depot, pickup_datetime = datetime.today(), drop_date = datetime.today() + timedelta(days=2), 
                                                        status = "Payment Success", cost = cost)
        TrackStatus(track_no = ts, status = "Payment Success").save()
        # messages.success(request, 'Payment Done Successfully! Depot pickup person contact you shortly')
        
        cost = int(float(cost)) * 100

        return render(request,'cust_paynow.html',{'cost' : cost })
@csrf_exempt
def payment_success(request):
    messages.success(request, 'Payment Done Successfully! Depot pickup person contact you shortly')
    return redirect('customer-dashboard')

def cust_login(request):
    lForm = CustLoginForm()
    if request.method == 'POST':
        lForm = CustLoginForm(request.POST)
        if lForm.is_valid():
                uname = lForm.cleaned_data['username']
                password = lForm.cleaned_data['password']
                user = authenticate(request, username=uname, password=password)

                if user is None:
                    print('Username or Password is Incorrect')
                    return render(request, 'cust_login.html', {'form': lForm, 'flag': True, 'msg': 'Username or Password is Incorrect'})

                if user.groups.filter(name='customer').exists():
                    login(request, user)
                    return redirect('/customer-dashboard')
                else:
                    print('You are not user for this portal')
                    return render(request, 'cust_login.html', {'form': lForm, 'flag': True, 'msg': 'You are not user for this portal'})
    return render(request, 'cust_login.html', {'form' : lForm, 'flag' : False})



def cust_register(request):

    userForm = CustomerRegForm()
    userProfForm = CustomerProfForm()

    flag = False

    if request.method == 'POST':
        userForm = CustomerRegForm(request.POST)
        userProfForm = CustomerProfForm(request.POST)

        if userForm.is_valid() and userProfForm.is_valid():
            # user = usrRegForm.save(commit=False)

            fname = userForm.cleaned_data['first_name']
            lname = userForm.cleaned_data['last_name']
            uname = userForm.cleaned_data['username']
            email = userForm.cleaned_data['email']
            password = userForm.cleaned_data['password']

            user = User.objects.create_user(
                uname, email, password)

            user.last_name = lname
            user.first_name = fname
            user.save()


            custGroup = Group.objects.get(name='customer')
            custGroup.user_set.add(user)

            cno = userProfForm.cleaned_data['contact']
            address = userProfForm.cleaned_data['address']
            city = userProfForm.cleaned_data['city']
            pincode = userProfForm.cleaned_data['zip']

            customer = Customer(user=user, contact=cno, 
                                      address=address, city=city, zip=pincode)

            customer.save()
            # messages.success(request, 'User Registration Successfuly Done')
            
            messages.success(request, 'Customer Registration Successfully Done')

            return redirect('/customer-login')

    return render(request, 'cust_register.html',{'usf' : userForm, 'upf' : userProfForm, 'flag' : flag})



    #   Depot-Employee Admin Controller/View
def depot_login(request):
    lForm = CustLoginForm()
    if request.method == 'POST':
        lForm = CustLoginForm(request.POST)
        if lForm.is_valid():
                uname = lForm.cleaned_data['username']
                password = lForm.cleaned_data['password']
                user = authenticate(request, username=uname, password=password)

                if user is None:
                    print('Username or Password is Incorrect')
                    return render(request, 'depot_login.html', {'form': lForm, 'flag': True, 'msg': 'Username or Password is Incorrect'})

                if user.groups.filter(name='depot_admin').exists():
                    login(request, user)
                    return redirect('/depot-dash')
                else:
                    print('You are not user for this portal')
                    return render(request, 'depot_login.html', {'form': lForm, 'flag': True, 'msg': 'You are not user for this portal'})
    return render(request, 'depot_login.html', {'form' : lForm, 'flag' : False})

@login_required(login_url='depot-login')
def depot_dashboard(request):
    return render(request, 'depot_dash.html')


@login_required(login_url='depot-login')
def depot_package(request):
    emp = Employee.objects.get(user = request.user)
    # depot = Depot.objects.get(depot=emp.depot)
    pck = PackageDetail.objects.filter(pick_up_depot = emp.depot)
    return render(request, 'depot_packages.html', {'package' : pck})



@login_required(login_url='company-login')
@is_depot_admin
def depot_edit_packages(request, id):
    package = PackageDetail.objects.get(id = id)

    if request.method == 'POST':
        status = request.POST['status']

        PackageDetail.objects.filter(id=id).update(status = status)
        TrackStatus(status = status, track_no = package.track_no).save()

        messages.success(request, 'Package updated Successfully')

        return redirect('depot-package')

    return render(request, 'depot_edit_package.html', {'package' : package})




# @login_required(login_url='company-login')
# @is_admin
# def comp_see_packages(request, id):
#     depot = Depot.objects.get(id=id)
#     pck = PackageDetail.objects.filter(pick_up_depot = depot)
#     return render(request, 'company_packages.html', {'package' : pck})












 #  Company Controllers/Views


def company_create(request):

    compForm = CustomerRegForm()
    compAdminForm = CompanyCreateForm()

    flag = False

    if request.method == 'POST':
        compForm = CustomerRegForm(request.POST)
        compAdminForm = CompanyCreateForm(request.POST)

        if compForm.is_valid() and compAdminForm.is_valid():
            # user = usrRegForm.save(commit=False)

            fname = compForm.cleaned_data['first_name']
            lname = compForm.cleaned_data['last_name']
            uname = compForm.cleaned_data['username']
            email = compForm.cleaned_data['email']
            password = compForm.cleaned_data['password']

            user = User.objects.create_user(
                uname, email, password)

            user.last_name = lname
            user.first_name = fname
            user.save()


            custGroup = Group.objects.get(name='company_admin')
            custGroup.user_set.add(user)

            cno = compAdminForm.cleaned_data['contact']
            name = compAdminForm.cleaned_data['name']
            company_email = compAdminForm.cleaned_data['company_email']
            address = compAdminForm.cleaned_data['address']
            city = compAdminForm.cleaned_data['city']
            pincode = compAdminForm.cleaned_data['zip']

            # customer = Company(company_admin=user, name = name , email = email contact=cno, 
            #                           address=address, city=city, zip=pincode)

            company = Company(company_admin = user, name = name, zip = pincode, 
                                address = address, contact = cno, city = city, company_email = company_email)

            company.save()
            # messages.success(request, 'User Registration Successfuly Done')
            
            messages.success(request, 'Company Registration Successfully Done')

            return redirect('/customer-login')

    return render(request, 'company_create.html', {'cuf' : compForm, 'cpf' : compAdminForm, 'flag' : flag})

def company_login(request):
    lForm = CustLoginForm()
    if request.method == 'POST':
        lForm = CustLoginForm(request.POST)
        if lForm.is_valid():
                uname = lForm.cleaned_data['username']
                password = lForm.cleaned_data['password']
                user = authenticate(request, username=uname, password=password)

                if user is None:
                    print('Username or Password is Incorrect')
                    return render(request, 'company_login.html', {'form': lForm, 'flag': True, 'msg': 'Username or Password is Incorrect'})

                if user.groups.filter(name='company_admin').exists():
                    login(request, user)
                    return redirect('/company-dashboard')
                else:
                    print('You are not company admin')
                    return render(request, 'company_login.html', {'form': lForm, 'flag': True, 'msg': 'You are not admin'})
    return render(request, 'company_login.html', {'form' : lForm, 'flag' : False})

@login_required(login_url='company-login')
@is_admin
def company_dash(request):
    return render(request, 'company_dash.html')


@login_required(login_url='company-login')
@is_admin
def make_depot_admin(request, id):
    emp = User.objects.get(id=id)
    usrGroup = Group.objects.get(name='depot_admin')
    usrGroup.user_set.add(emp)
    messages.success(request, 'Employee become Depot Admin now')
    return redirect('/our-depot')


@login_required(login_url='company-login')
@is_admin
def comp_create_emp(request):
    company = Company.objects.filter(company_admin = request.user).first()
    depot = Depot.objects.filter(company = company)
    upf = CustomerProfForm()
    urf = CustomerRegForm()


    if request.method == 'POST':
        urf = CustomerRegForm(request.POST)
        upf = CustomerProfForm(request.POST)

        if urf.is_valid() and upf.is_valid():
            # user = usrRegForm.save(commit=False)

            fname = urf.cleaned_data['first_name']
            lname = urf.cleaned_data['last_name']
            uname = urf.cleaned_data['username']
            email = urf.cleaned_data['email']
            password = urf.cleaned_data['password']

            user = User.objects.create_user(
                uname, email, password)

            user.last_name = lname
            user.first_name = fname
            user.save()


            custGroup = Group.objects.get(name='employee')
            custGroup.user_set.add(user)


            did = request.POST.get('depot')

            depot = Depot.objects.get(id = did)

            cno = upf.cleaned_data['contact']
            address = upf.cleaned_data['address']
            city = upf.cleaned_data['city']
            pincode = upf.cleaned_data['zip']

            customer = Employee(user=user, depot = depot, contact=cno, 
                                      address=address, city=city, zip=pincode)

            customer.save()
            
            messages.success(request, 'Employee Registration Successfully Done')

            return redirect('/company-dashboard')
    return render(request, 'company_add_employee.html', {'upf' : upf, 'urf' : urf, 'depot' : depot})


@login_required(login_url='company-login')
@is_admin
def comp_depot(request):
    company = Company.objects.get(company_admin = request.user)
    depot = Depot.objects.filter(company = company)

    return render(request, 'company_depots.html', {'depots' : depot})

@login_required(login_url='company-login')
@is_admin
def comp_employees(request, id):
    depot = Depot.objects.get(id = id)
    emps = Employee.objects.filter(depot=depot)
    print(emps)
    return render(request, 'company_employees.html', {'emps' : emps})

@login_required(login_url='company-login')
@is_admin
def comp_see_packages(request, id):
    depot = Depot.objects.get(id=id)
    pck = PackageDetail.objects.filter(pick_up_depot = depot)
    return render(request, 'company_packages.html', {'package' : pck})


@login_required(login_url='company-login')
@is_admin
def comp_edit_packages(request, id):
    package = PackageDetail.objects.get(id = id)

    if request.method == 'POST':
        status = request.POST['status']

        PackageDetail.objects.filter(id=id).update(status = status)
        TrackStatus(status = status, track_no = package.track_no).save()

        messages.success(request, 'Package updated Successfully')

        return redirect('our-depot')

    return render(request, 'company_edit_package.html', {'package' : package})




@login_required(login_url='company-login')
@is_admin
def comp_create_depot(request):
    createDepotForm = CompanyCreateDepot()

    if request.method == 'POST':
        createDepotForm = CompanyCreateDepot(request.POST)
        if createDepotForm.is_valid():
            
            company = Company.objects.filter(company_admin = request.user).first()

            contact = createDepotForm.cleaned_data['contact']
            zip = createDepotForm.cleaned_data['zip']
            city = createDepotForm.cleaned_data['city']
            address = createDepotForm.cleaned_data['address']

            depot = Depot(company = company, contact = contact, address = address, city = city, zip = zip)
            depot.save()

            messages.success(request, 'Depot added successfully')

            return redirect('/our-depot')

    return render(request, 'company_create_depot.html', {'form' : createDepotForm})