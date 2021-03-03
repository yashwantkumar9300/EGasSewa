from django.http import JsonResponse
from django.shortcuts import render,redirect
import random
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import razorpay
from app.models import * #AdminModel,State,District,Customer,Distributor,DistributorAgency,PriceModel
from django.core.mail import send_mail
from django.db.models import Max
from app.SendOtp import sendASMS
from EGasSeva.settings import EMAIL_HOST_USER


def distributorIdno():
    res = Distributor.objects.all().aggregate(Max('idno'))
    if res['idno__max']:
        idno = res['idno__max']+1
        return idno
    else:
        return 12450001

def userIdno():
    res = Customer.objects.all().aggregate(Max('idno'))
    if res['idno__max']:
        idno = res['idno__max'] + 1
        return idno
    else:
        return 72450001

def ref_generator():
    rno = random.randint(10000000,99999999)
    return rno

def otpGenerator():
    otp = random.randint(100000,999999)
    return otp

EMAIL_OTP = ""
MOBILE_OTP = ""

def showIndex(request):
    return render(request,"index.html")

def admin_login(request):
    return render(request,"admin_login.html")

def admin_login_check(request):
    uname = request.POST.get("t1")
    upas = request.POST.get("t2")
    if request.method == "POST":
        try:
            AdminModel.objects.get(username=uname,password=upas)
            request.session["admin_status"] = True
            return redirect('admin_home')
        except AdminModel.DoesNotExist:
            return render(request,"admin_login.html",{"error":"Invalid User"})
    else:
        request.session["admin_status"] = False
        return admin_login(request)


def admin_home(request):
    return render(request,"admin_home.html")

def admin_pass_form(request):
    return render(request,"admin_pass_form.html")

def admin_change_pass(request):
    oldpas = request.POST.get("t1")
    newpas = request.POST.get("t2")
    try:
        res = AdminModel.objects.get(password=oldpas)
        res.password = newpas
        res.save()
        # AdminModel.objects.filter(password=oldpas).update(password=newpas)
        return render(request,"admin_pass_form.html",{"msg":"Password Changed Successfully"})
    except AdminModel.DoesNotExist:
        return render(request,"admin_pass_form.html",{"error":"Invalid Old Password"})

def add_state(request):
    return render(request, "add_state.html",{"state":State.objects.all()})

def save_state(request):
    try:
        State(state_name=request.POST.get("t1")).save()
        return render(request,"add_state.html",{"msg":"State is Saved","state":State.objects.all()})
    except IntegrityError:
        return render(request,"add_state.html",{"msg":"State Allready Saved","state":State.objects.all()})

def view_dealers(request):
    res = Distributor.objects.all()
    return render(request, "view_distributor.html", {"data":res})

def dealer_approval(request):
    res = Distributor.objects.get(idno=request.POST.get("t1"))
    res.status = "Approved"
    res.save()
    sendASMS(str(res.mobile), "Your E Gas Sewa Registration Accepted and Distributor Id is : " + str(res.idno))
    return view_dealers(request)

def dealer_decline(request):
    res = Distributor.objects.get(idno=request.POST.get("t1"))
    res.status = "Cancel"
    res.save()
    sendASMS(str(res.mobile), "Your E Gas Sewa Registration is Rejected")
    return view_dealers(request)

def add_district(request):
    return render(request,"add_district.html",{"s_data":State.objects.all(),"district":District.objects.all()})

def save_district(request):
    state_id = request.POST.get("t1")
    dict = request.POST.get("t2")
    try:
        District(dict_name=dict,dict_state_id=state_id).save()
        return add_district(request)
    except IntegrityError:
        return render(request,"add_district.html",{"msg":"District Allready Saved","s_data":State.objects.all(),"district":District.objects.all()})

def add_price(request):
    return render(request,"add_price.html",{"price":PriceModel.objects.all()})

def save_price(request):
    price = request.POST.get("t1")
    date = request.POST.get("t2")
    PriceModel(price=price,date=date).save()
    return redirect('add_price')

# def dealer_address(request):
#     return render(request, "dealer_address.html",{"form":DealerAddressForm()})
def dealer_address(request):
    return render(request, "distributor_address1.html", {"s_data":State.objects.all(),"agency":DistributorAgency.objects.all()})

def save_dealer_address(request):
    sid = request.POST.get("t1")
    did = request.POST.get("t2")
    idno = request.POST.get("t3")
    agencyname = request.POST.get("t4")
    try:
        DistributorAgency(d_id=idno,agency_name=agencyname,district_id=did,state_id=sid).save()
        # print(sid,did,idno,agencyname)
        return dealer_address(request)
    except IntegrityError:
        return render(request,"distributor_address1.html",{"msg":"Agency Allready saved","s_data":State.objects.all(),"agency":DistributorAgency.objects.all()})

def view_connection(request):
    return render(request,"view_connection.html",{"data":Customer.objects.all()})

def aboutus(request):
    return render(request,"aboutus.html")

def contactus(request):
    return render(request,"contactus.html")


def distributor_login(request):
    return render(request, "distributor_login.html")

def distributor_login_check(request):
    uname = request.POST.get("t1")
    upas = request.POST.get("t2")
    if request.method == "POST":
        try:
            res = Distributor.objects.get(username=uname,password=upas)
            if res.status == "Approved":
                request.session['dealer_id'] = res.idno
                return redirect('distributor_home')
            elif res.status == "Pending":
                return render(request, "distributor_login.html", {"msg": "Your Registration is Pending"})
            else:
                return render(request, "distributor_login.html", {"msg": "Your Registration is Regected"})
        except Distributor.DoesNotExist:
            return render(request, "distributor_login.html", {"error": "Invalid User"})
    else:
        del request.session['dealer_id']
        return distributor_login(request)

def distributor_home(request):
    return render(request, "distributor_home.html",{"data":Distributor.objects.get(idno=request.session["dealer_id"])})

def distributor_register(request):
    return render(request, "distributor_register.html", {"s_data":State.objects.all()})

d_fname,d_lname,d_ftname,d_dob,d_gen,d_uname,d_pass,d_mobile,d_email,d_house  = "","","","","","","","","",""
d_street,d_city,d_state,d_district,d_pin,d_id_proof,d_idno,d_add_proof,d_add_idno,d_agencyname  = "","","","","","","","","",""
d_agency_reg,d_agency_add,d_idproof,d_addproof,d_photo,d_ajencyphoto = "","","","","",""
refno = ""

def distributor_save(request):
    global d_fname,d_lname,d_ftname,d_dob,d_gen,d_uname,d_pass,d_mobile,d_email,d_house
    global d_street, d_city, d_state, d_district, d_pin, d_id_proof, d_idno, d_add_proof, d_add_idno, d_agencyname
    global d_agency_reg, d_agency_add, d_idproof, d_addproof, d_photo, d_ajencyphoto
    d_fname = request.POST.get("d1")
    d_lname = request.POST.get("d2")
    d_ftname = request.POST.get("d3")
    d_dob = request.POST.get("d4")
    d_gen = request.POST.get("d5")
    d_uname= request.POST.get("d6")
    d_pass = request.POST.get("d7")
    d_mobile = request.POST.get("d9")
    d_email = request.POST.get("d10")
    d_house = request.POST.get("d11")
    d_street = request.POST.get("d12")
    d_city = request.POST.get("d13")
    d_state = request.POST.get("d14")
    d_district = request.POST.get("d15")
    d_pin = request.POST.get("d16")
    d_id_proof = request.POST.get("d17")
    d_idno = request.POST.get("d18")
    d_add_proof = request.POST.get("d19")
    d_add_idno = request.POST.get("d20")
    d_agencyname = request.POST.get("d21")
    d_agency_reg = request.POST.get("d22")
    d_agency_add = request.POST.get("d23")
    d_idproof = request.FILES["d24"]
    d_addproof = request.FILES["d25"]
    d_photo = request.FILES["d26"]
    d_ajencyphoto = request.FILES["d27"]

    global EMAIL_OTP,MOBILE_OTP,refno
    EMAIL_OTP = otpGenerator()
    MOBILE_OTP = otpGenerator()
    sendASMS(str(d_mobile), "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP))
    send_to = d_email.split(",")
    send_to_subject = "Registration OTP"
    send_to_message = "Your E Gas Sewa Registration OTP is : " + str(EMAIL_OTP)
    send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to,fail_silently=False)
    idno = distributorIdno()
    refno = ref_generator()
    try:
        Distributor(idno=idno, fname=d_fname, lname=d_lname, ftname=d_ftname, dob=d_dob, gender=d_gen, username=d_uname,password=d_pass,
                    mobile=d_mobile, email=d_email, house=d_house, street=d_street, city=d_city, state_id=d_state,district_id=d_district,
                    pincode=d_pin, id_proof=d_id_proof, id_number=d_idno, add_proof=d_add_proof, add_id=d_add_idno,agenncy_name=d_agencyname,
                    agency_reg=d_agency_reg, agency_add=d_agency_add, id_file=d_idproof, add_file=d_addproof, photo=d_photo,
                    agency_file=d_ajencyphoto, reference=refno).save()
        print(EMAIL_OTP)
        print(MOBILE_OTP)
        return render(request,"otp_validation.html")
    except IntegrityError:
        return render(request, "distributor_register.html", {"s_data":State.objects.all(),"msg":"Distributor Allready Registerd"})


def validate_distributor_otp(request):
    email_otp = int(request.POST.get("t1"))
    mobile_otp = int(request.POST.get("t2"))
    if EMAIL_OTP == email_otp and MOBILE_OTP == mobile_otp:
        # print(idno,refno,d_fname, d_lname, d_ftname, d_dob, d_gen, d_uname, d_pass, d_mobile, d_email, d_house,
        #       d_street, d_city, d_state, d_district, d_pin, d_id_proof, d_idno, d_add_proof, d_add_idno, d_agencyname,
        #       d_agency_reg, d_agency_add, d_idproof, d_addproof, d_photo, d_ajencyphoto)
        sendASMS(str(d_mobile), "Your E Gas Sewa Registration Reference Number is : " + str(refno))
        return render(request, "message.html", {"msg": "Registration is Successfull","refno":refno})
    else:
        return render(request,"otp_validation.html",{"msg":"Invalid OTP! Please Enter Valid OTP"})

def resend_otp(request):
    global EMAIL_OTP, MOBILE_OTP
    EMAIL_OTP = otpGenerator()
    MOBILE_OTP = otpGenerator()
    sendASMS(str(d_mobile), "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP))
    send_to = d_email.split(",")
    send_to_subject = "Registration OTP"
    send_to_message = "Your E Gas Sewa Registration OTP is : " + str(EMAIL_OTP)
    send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to,fail_silently=False)
    return render(request, "otp_validation.html")

def distributor_status(request):
    return render(request,"distributor_status.html")

def distributor_check_status(request):
    reference = request.POST.get("c1")
    dob = request.POST.get("c2")
    try:
        res = Distributor.objects.get(reference=reference,dob=dob)
        if res.status == "Approved":
            return render(request,"distributor_status.html",{"msg":"Your Registration is Accepted"})
        elif res.status == "Pending":
            return render(request, "distributor_status.html",{"msg":"Your Registration is Pending"})
        else:
            return render(request,"distributor_status.html",{"msg":"Youe Registration is Rejected"})
    except Distributor.DoesNotExist:
        return render(request, "distributor_status.html", {"msg":"Invalid Details"})


def distributor_pass_form(request):
    return render(request, "distributor_pass_form.html")

def distributor_change_pass(request):
    oldpas = request.POST.get("t1")
    newpas = request.POST.get("t2")
    try:
        res = Distributor.objects.get(password=oldpas,idno=request.session['dealer_id'])
        res.password = newpas
        res.save()
        return render(request, "distributor_pass_form.html", {"msg": "Password Changed Successfully"})
    except Distributor.DoesNotExist:
        return render(request, "distributor_pass_form.html", {"error": "Invalid Old Password"})

def distributor_forgot_pass(request):
    return render(request, "distributor_forgot_pass.html")

def distributor_forgot_password(request):
    mob = request.POST.get("t1")
    email = request.POST.get("t2")
    try:
        res = Distributor.objects.get(mobile=mob,email=email)
        send_to = request.POST.get("t2").split(",")
        send_to_subject = "Forgot Password"
        send_to_message = "Your E Gas Sewa Password is : " + str(res.password)
        send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to,fail_silently=False)
        sendASMS(str(mob), "Your E Gas Sewa Password is : " + str(res.password))
        return render(request, "distributor_forgot_pass.html", {"msg": "Password Send Your Registered Email-Id and Mobile No"})
    except Distributor.DoesNotExist:
        return render(request, "distributor_forgot_pass.html", {"error": "Invalid Details"})

def view_customer(request):
    return render(request,"view_customer.html",{"data":Customer.objects.filter(distributor_id=request.session["dealer_id"])})

def customer_approval(request):
    res = Customer.objects.get(idno=request.POST.get("t1"))
    res.status = "Approved"
    res.save()
    sendASMS(str(res.mobile), "Your E Gas Sewa Registration Accepted and Cunsumer Id is : " + str(res.idno))
    return view_customer(request)

def customer_cancel(request):
    res = Customer.objects.get(idno=request.POST.get("t1"))
    res.status = "Cancel"
    res.save()
    sendASMS(str(res.mobile), "Your E Gas Sewa Registration is Rejected")
    return view_customer(request)


def user_register(request):
    return render(request,"user_register.html",{"s_data":State.objects.all()})

u_fname,u_lname,u_ftname,u_dob,u_gen,u_mobile,u_email,u_house  = "","","","","","","",""
u_street,u_city,u_state,u_district,u_pincode,u_id_proof,u_idno,u_add_proof,u_add_idno = "","","","","","","","",""
u_idproof,u_addproof,u_photo,state_id,district_id,dist_id,u_cylinder,u_connection = "","","","","","","",""
u_refno = ""

def user_save(request):
    global u_fname,u_lname,u_ftname,u_dob,u_gen,u_mobile,u_email,u_house
    global u_street,u_city,u_state,u_district,u_pincode,u_id_proof,u_idno,u_add_proof,u_add_idno
    global u_idproof,u_addproof,u_photo,state_id,district_id,dist_id,u_cylinder,u_connection
    state_id = request.POST.get("t1")
    district_id = request.POST.get("t2")
    dist_id = request.POST.get("c3")
    u_fname = request.POST.get("t4")
    u_lname = request.POST.get("t5")
    u_ftname = request.POST.get("t6")
    u_dob = request.POST.get("t7")
    u_gen = request.POST.get("t8")
    u_mobile = request.POST.get("t9")
    u_email = request.POST.get("t10")
    u_house = request.POST.get("t11")
    u_street = request.POST.get("t12")
    u_city = request.POST.get("t13")
    u_state = request.POST.get("t14")
    u_district = request.POST.get("t15")
    u_pincode = request.POST.get("t16")
    u_cylinder = request.POST.get("t17")
    u_connection = request.POST.get("t18")
    u_id_proof = request.POST.get("t19")
    u_idno = request.POST.get("t20")
    u_add_proof = request.POST.get("t21")
    u_add_idno = request.POST.get("t22")
    u_idproof = request.FILES["t23"]
    u_addproof = request.FILES["t24"]
    u_photo = request.FILES["t25"]

    global MOBILE_OTP,u_refno
    MOBILE_OTP = otpGenerator()
    sendASMS(str(u_mobile), "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP))
    send_to = u_email.split(",")
    send_to_subject = "Registration OTP"
    send_to_message = "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP)
    send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to,fail_silently=False)
    idno = userIdno()
    u_refno = ref_generator()
    try:
        Customer(idno=idno, fname=u_fname, lname=u_lname, ftname=u_ftname, dob=u_dob, gender=u_gen, mobile=u_mobile,email=u_email,
                 house=u_house, street=u_street, city=u_city, cstate=u_state, cdistrict=u_district, pincode=u_pincode,cylinder=u_cylinder,
                 connection=u_connection, id_proof=u_id_proof, id_number=u_idno, add_proof=u_add_proof, add_id=u_add_idno,id_file=u_idproof,
                 add_file=u_addproof, photo=u_photo, state_id=state_id, district_id=district_id, distributor_id=dist_id,reference=u_refno).save()
        print(MOBILE_OTP)
        return render(request,"user_otp_validation.html")
    except IntegrityError:
        return render(request,"user_register.html",{"s_data":State.objects.all(),"msg":"Customer Allready saved"})


def validate_user_otp(request):
    otp = int(request.POST.get("t1"))
    if MOBILE_OTP == otp:
        # print(idno, u_refno,state_id,district_id,dist_id,u_fname,u_lname,u_ftname,u_dob,u_gen,u_mobile,u_email,u_house,
        #       u_street,u_city,u_state,u_district,u_pincode,u_cylinder,u_connection,u_id_proof,u_idno,u_add_proof,u_add_idno,
        #       u_idproof,u_addproof,u_photo)
        sendASMS(str(u_mobile), "Your E Gas Sewa Registration Reference Number is : " + str(u_refno))
        return render(request, "user_message.html", {"msg": "Registered Successfully","urefno":u_refno})
    else:
        return render(request, "user_otp_validation.html", {"msg": "Invalid OTP! Please Enter Valid OTP"})

def user_resend_otp(request):
    global MOBILE_OTP
    MOBILE_OTP = otpGenerator()
    sendASMS(str(u_mobile), "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP))
    send_to = u_email.split(",")
    send_to_subject = "Registration OTP"
    send_to_message = "Your E Gas Sewa Registration OTP is : " + str(MOBILE_OTP)
    send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to,fail_silently=False)
    return render(request, "user_otp_validation.html")

def user_status(request):
    return render(request,"user_status.html")

def user_check_status(request):
    reference = request.POST.get("c1")
    dob = request.POST.get("c2")
    try:
        res = Customer.objects.get(reference=reference, dob=dob)
        if res.status == "Approved":
            return render(request, "user_status.html", {"msg": "Your Registration is Accepted"})
        elif res.status == "Pending":
            return render(request, "user_status.html", {"msg": "Your Registration is Pending"})
        else:
            return render(request, "user_status.html", {"msg": "Youe Registration is Rejected"})
    except Customer.DoesNotExist:
        return render(request, "user_status.html", {"msg": "Invalid Details"})


def user_login(request):
    return render(request,"user_login.html")

def user_login_check(request):
    email = request.POST.get("t1")
    cid = request.POST.get("t2")
    if request.method == "POST":
        try:
            res = Customer.objects.get(email=email,idno=cid)
            if res.status == "Approved":
                request.session['user_id'] = res.idno
                return redirect('user_home')
            else:
                return render(request,"user_login.html",{"error":"Sorry! Your Account is Not Active"})
        except Customer.DoesNotExist:
            return render(request,"user_login.html",{"error":"Invalid User"})
    else:
        del request.session['user_id']
        return redirect('main')


def user_home(request):
    res = Customer.objects.get(idno=request.session['user_id'])
    dist = Distributor.objects.get(idno=res.distributor_id)
    return render(request,"user_home.html",{"data":res,"data1":dist})

def user_forgot_pass(request):
    return render(request,"user_forgot_pass.html")

def user_forgot_password(request):
    mob = request.POST.get("t1")
    email = request.POST.get("t2")
    try:
        res = Customer.objects.get(mobile=mob, email=email)
        send_to = request.POST.get("t2").split(",")
        send_to_subject = "Forgot Password"
        send_to_message = "Your E Gas Sewa Consumer Number is : " + str(res.idno)
        send_mail(send_to_subject, send_to_message, EMAIL_HOST_USER, send_to)
        sendASMS(str(mob), "Your E Gas Sewa Consumer Number is : " + str(res.idno))
        return render(request, "user_forgot_pass.html", {"msg": "Consumer Number Send Your Registered Email-Id and Mobile No"})
    except Customer.DoesNotExist:
        return render(request, "user_forgot_pass.html", {"error": "Invalid Details"})


def quick_book(request):
    if request.session.get('user_id'):
        res = Customer.objects.get(idno=request.session['user_id'])
        dist = Distributor.objects.get(idno=res.distributor_id)
        return render(request,"book_cylinder.html",{"data": res,"data1":dist,"price":PriceModel.objects.all()})
    else:
        return render(request,"quick_book.html",{"s_data":State.objects.all(),"price":PriceModel.objects.all()})

def quick_pay(request):
    sid = request.POST.get("t1")
    did = request.POST.get("t2")
    cid = request.POST.get("c3")
    cusid = request.POST.get("t4")
    try:
        res = Customer.objects.get(state_id=sid,district_id=did,distributor_id=cid,idno=cusid)
        return render(request,"quick_pay.html",{"data":res,"price":PriceModel.objects.all()})
    except Customer.DoesNotExist:
        return render(request,"quick_book.html",{"msg":"Invalid Consumer Number"})

def book_now(request):
    if request.session.get('user_id'):
        res = Customer.objects.get(idno=request.session['user_id'])
        dist = Distributor.objects.get(idno=res.distributor_id)
        return render(request,"book_cylinder.html",{"data": res,"data1":dist,"price":PriceModel.objects.all()})
    else:
        return redirect('user_login')


def payment_page(request):
    mob = request.POST.get("t1")
    price = float(request.POST.get("t2"))
    cid = request.POST.get("t3")
    did = request.POST.get("t4")
    amount = price * 100
    currency = 'INR'
    receipt = 'order_rcptid_11'
    client = razorpay.Client(auth=("rzp_test_0AztplFyH9hQyL","WDnNp7Fuv5Hp1gSoR7drwxop"))
    payment = client.order.create(dict(amount=amount, currency=currency, receipt=receipt,payment_capture='1'))
    PaymentModel(reference=payment['created_at'],paymentid=payment['id'],customer_id=cid,distributor_id=did,mobile=mob,price=price).save()
    # print(mob,price,cid,did, payment['id'],payment['created_at'])
    # print(cid, did,price,payment['id'],payment['created_at'],"1")
    OrderModel(reference=payment['created_at'],paymentid=payment['id'],customer_id=cid,distributor_id=did,quantity=1,price=price).save()
    return render(request,"payment_page.html" ,{"payment":payment,"orderid":payment['id']})


@method_decorator(csrf_exempt,name="dispatch")
def success_payment(request):
    global orderid
    orderid = ""
    success = request.POST
    paymentid = request.POST.get("orderid")
    for k,v in success.items():
        if k == "razorpay_order_id":
            orderid = v
            break
    if orderid == paymentid:
        res = PaymentModel.objects.get(paymentid=paymentid)
        res.status = "Success"
        res.save()
        if request.session.get('user_id'):
            return render(request,"payment_success.html",{"msg":"Pyament Success" })
        else:
            return render(request, "payment_success1.html", {"msg": "Pyament Success"})
    else:
        return render(request,"payment_success.html",{"msg":"Pyament Failer" })


def load_district(request):
    sid = request.GET.get('stateid')
    district = District.objects.filter(dict_state_id=sid)
    return render(request, 'district_dropdown_list.html', {'district': district})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

def ajax_load_distributor(request):
    sid = request.GET.get('dictid')
    res = DistributorAgency.objects.filter(district_id=sid)
    return render(request,"distributor_dropdown.html",{'distributor': res})


@method_decorator(csrf_exempt,name="dispatch")
def checkOne(request):
    name = request.POST.get('cname')
    try:
        Distributor.objects.get(username=name)
        res = {"error": "User Name is Taken"}
    except Distributor.DoesNotExist:
        res = {"message": "User Name is Available"}
    return JsonResponse(res)

@method_decorator(csrf_exempt,name="dispatch")
def checkmobile(request):
    mob = request.POST.get('cname')
    try:
        Distributor.objects.get(mobile=mob)
        res = {"error": "Mobile Number Allready Registerd"}
    except Distributor.DoesNotExist:
        res = {"message": "Mobile No is Available"}
    return JsonResponse(res)

@method_decorator(csrf_exempt,name="dispatch")
def checkemail(request):
    email = request.POST.get('cname')
    try:
        Distributor.objects.get(email=email)
        res = {"error": "Email-Id is Allready Registerd"}
    except Distributor.DoesNotExist:
        res = {"message": "Email-Id is Available"}
    return JsonResponse(res)

@method_decorator(csrf_exempt,name="dispatch")
def check_user_mobile(request):
    mob = request.POST.get('cname')
    try:
        Customer.objects.get(mobile=mob)
        res = {"error": "Mobile Number Allready Registerd"}
    except Customer.DoesNotExist:
        res = {"message": "Mobile No is Available"}
    return JsonResponse(res)

@method_decorator(csrf_exempt,name="dispatch")
def check_user_email(request):
    email = request.POST.get('cname')
    try:
        Customer.objects.get(email=email)
        res = {"error": "Email-Id is Allready Registerd"}
    except Customer.DoesNotExist:
        res = {"message": "Email-Id is Available"}
    return JsonResponse(res)

# @method_decorator(csrf_exempt,name="dispatch")
# def statedata(request):
#     dict_data = { }
#     sid = request.POST.get('state')
#     district = District.objects.filter(dict_state_id=sid)
#     for x in district:
#         d1 = {
#             x.dist_id:
#             x.dict_name
#         }
#         dict_data.update(d1)
#     #print(dict_data)
#     #json_data = json.dumps(dict_data)
#     #return render(request,"district_dropdown_list.html",{"dictrict":district})
#     #print(list(district.values('dist_id','dict_name')))
#     return JsonResponse(dict_data)

def view_booking(request):
    res = OrderModel.objects.filter(distributor_id=request.session['dealer_id'])
    return render(request,"view_booking.html",{"data":res})


def view_payment(request):
    res = PaymentModel.objects.filter(distributor_id=request.session['dealer_id'])
    return render(request,"view_payment.html",{"data":res})


def view_user_booking(request):
    res = OrderModel.objects.filter(customer_id=request.session['user_id'])
    return render(request,"view_user_booking.html",{"data":res})


def view_user_payment(request):
    res = PaymentModel.objects.filter(customer_id=request.session['user_id'])
    return render(request,"view_user_payment.html",{"data":res})


def approve_booking(request):
    res = OrderModel.objects.get(idno=request.POST.get("t1"))
    res.status = "Delivered"
    res.save()
    return redirect('view_booking')


def booking_report(request):
    return render(request,"booking_report.html")


def breport(request):
    fdate = request.POST.get("t1")
    tdate = request.POST.get("t2")
    res = OrderModel.objects.filter(date__gte=fdate,date__lte=tdate)
    return render(request,"breport.html",{"data":res})


def cust_breport(request):
    return render(request,"cust_breport.html")


def cust_report(request):
    fdate = request.POST.get("t1")
    tdate = request.POST.get("t2")
    res = OrderModel.objects.filter(date__gte=fdate, date__lte=tdate,distributor_id=request.session['dealer_id'])
    return render(request,"cust_report.html",{"data":res})