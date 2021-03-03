"""EGasSeva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from EGasSeva import settings
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.showIndex,name="main"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_login_check/',views.admin_login_check,name="admin_login_check"),
    path('admin_pass_form/',views.admin_pass_form,name="admin_pass_form"),
    path('admin_change_pass/',views.admin_change_pass,name="admin_change_pass"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('add_state/',views.add_state,name="add_state"),
    path('save_state/',views.save_state,name="save_state"),
    path('add_district/',views.add_district,name="add_district"),
    path('save_district/',views.save_district,name="save_district"),
    path('dealer_address/',views.dealer_address,name="dealer_address"),
    path('save_dealer_address/',views.save_dealer_address,name="save_dealer_address"),
    path('view_dealers/',views.view_dealers,name="view_dealers"),
    path('dealer_approval/',views.dealer_approval,name="dealer_approval"),
    path('dealer_decline/',views.dealer_decline,name="dealer_decline"),
    path('view_connection/',views.view_connection,name="view_connection"),
    path('add_price/',views.add_price,name="add_price"),
    path('save_price/',views.save_price,name="save_price"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('contactus/',views.contactus,name="contactus"),
    path('booking_report/',views.booking_report,name="booking_report"),
    path('breport/',views.breport,name="breport"),

    path('distributor_register/',views.distributor_register,name="distributor_register"),
    path('distributor_save/',views.distributor_save,name="distributor_save"),
    path('resend_otp/',views.resend_otp,name="resend_otp"),
    path('validate_distributor_otp/',views.validate_distributor_otp,name="validate_distributor_otp"),
    path('distributor_status/',views.distributor_status,name="distributor_status"),
    path('distributor_check_status/',views.distributor_check_status,name="distributor_check_status"),
    path('distributor_login/',views.distributor_login,name="distributor_login"),
    path('distributor_login_check/',views.distributor_login_check,name="distributor_login_check"),
    path('distributor_home/',views.distributor_home,name="distributor_home"),
    path('distributor_pass_form/',views.distributor_pass_form,name="distributor_pass_form"),
    path('distributor_change_pass/',views.distributor_change_pass,name="distributor_change_pass"),
    path('distributor_forgot_pass/',views.distributor_forgot_pass,name="distributor_forgot_pass"),
    path('distributor_forgot_password/', views.distributor_forgot_password, name="distributor_forgot_password"),
    path('view_customer/',views.view_customer,name="view_customer"),
    path('customer_approval/',views.customer_approval,name="customer_approval"),
    path('customer_cancel/',views.customer_cancel,name="customer_cancel"),
    path('view_booking/',views.view_booking,name="view_booking"),
    path('approve_booking/',views.approve_booking,name="approve_booking"),
    path('view_payment/',views.view_payment,name="view_payment"),
    path('cust_breport/',views.cust_breport,name="cust_breport"),
    path('cust_report/',views.cust_report,name="cust_report"),

    path('user_register/',views.user_register,name="user_register"),
    path('user_save/',views.user_save,name="user_save"),
    path('validate_user_otp/',views.validate_user_otp,name="validate_user_otp"),
    path('user_resend_otp/',views.user_resend_otp,name="user_resend_otp"),
    path('user_status/',views.user_status,name="user_status"),
    path('user_check_status/',views.user_check_status,name="user_check_status"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_login_check/',views.user_login_check,name="user_login_check"),
    path('user_home/',views.user_home,name="user_home"),
    path('user_forgot_pass/',views.user_forgot_pass,name="user_forgot_pass"),
    path('user_forgot_password/',views.user_forgot_password,name="user_forgot_password"),
    path('payment_page/',views.payment_page,name="payment_page"),
    path('success_payment/',views.success_payment,name="success_payment"),
    path('view_user_booking/',views.view_user_booking,name="view_user_booking"),
    path('view_user_payment/',views.view_user_payment,name="view_user_payment"),

    path('quick_book/',views.quick_book,name="quick_book"),
    path('quick_pay/',views.quick_pay,name="quick_pay"),
    path('book_now/',views.book_now,name="book_now"),

    path('ajax_load_district/',views.load_district,name="ajax_load_district"),
    path('ajax_load_distributor/',views.ajax_load_distributor,name="ajax_load_distributor"),
    path('checkOne/',views.checkOne,name="checkOne"),
    path('checkmobile/',views.checkmobile,name="checkmobile"),
    path('checkemail/',views.checkemail,name="checkemail"),
    path('check_user_mobile/',views.check_user_mobile,name="check_user_mobile"),
    path('check_user_email/',views.check_user_email,name="check_user_email")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)