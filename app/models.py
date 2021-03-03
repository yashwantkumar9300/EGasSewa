from django.db import models

class AdminModel(models.Model):
    idno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.state_name

class District(models.Model):
    dist_id = models.AutoField(primary_key=True)
    dict_name = models.CharField(max_length=50, unique=True)
    dict_state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.dict_name

class DistributorAgency(models.Model):
    d_id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,default=False)
    district = models.ForeignKey(District,on_delete=models.CASCADE,default=False)
    agency_name = models.TextField(max_length=200, unique=True)

    def __str__(self):
        return self.agency_name


class CommonModel(models.Model):
    idno = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    ftname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=50)
    mobile = models.IntegerField(unique=True)
    email = models.EmailField(max_length=100,unique=True)
    house = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    pincode = models.IntegerField()
    id_proof = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50,unique=True)
    add_proof = models.CharField(max_length=50)
    add_id = models.CharField(max_length=50,unique=True)
    reference = models.IntegerField()
    status = models.CharField(max_length=50,default="Pending")
    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Distributor(CommonModel):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    agenncy_name = models.CharField(max_length=100,unique=True)
    agency_reg = models.CharField(max_length=50,unique=True)
    agency_add = models.TextField()
    id_file = models.FileField(upload_to="distributor_File/")
    add_file = models.FileField(upload_to="distributor_File/")
    photo = models.FileField(upload_to="distributor_File/")
    agency_file = models.FileField(upload_to="distributor_File/")


class Customer(CommonModel):
    distributor = models.ForeignKey(DistributorAgency,on_delete=models.CASCADE)
    cstate = models.CharField(max_length=50)
    cdistrict = models.CharField(max_length=50)
    cylinder = models.CharField(max_length=50)
    connection = models.CharField(max_length=50)
    id_file = models.FileField(upload_to="customer_File/")
    add_file = models.FileField(upload_to="customer_File/")
    photo = models.FileField(upload_to="customer_File/")

class PriceModel(models.Model):
    idno = models.AutoField(primary_key=True)
    price= models.FloatField()
    date = models.DateField()

class PaymentModel(models.Model):
    idno = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.IntegerField()
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor,on_delete=models.CASCADE)
    mobile = models.IntegerField()
    price = models.FloatField()
    paymentid = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default='Failed')

class OrderModel(models.Model):
    idno = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    reference = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    paymentid = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')
