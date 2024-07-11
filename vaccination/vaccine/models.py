from django.db import models

# Create your models here.
class login(models.Model):
    log_id= models.AutoField(primary_key=True)
    username = models.CharField("username",max_length=100)
    password =models.CharField("password",max_length=100)
    role=models.CharField("role",max_length=100)

    def __str__(self):
        return self.username
#med_id,med_name,med_pic,med_company,med_exp,med_price,med_stock,med_type,med_unit

class Phrama(models.Model):
   PhramaStaff_id= models.AutoField(primary_key=True)
   PhramaStaff_name= models.CharField("Name",max_length=100)
   PhramaStaff_gender = models.CharField("Staff_gender", max_length=100)
   PhramaStaff_address = models.CharField("Staff_address", max_length=500)
   PhramaStaff_email = models.EmailField("Staff_email", max_length=200)
   PhramaStaff_phone=models.CharField("Staff_phone",max_length=100)
   PhramaStaff_qualification = models.CharField("Staff_qualification", max_length=200)
   PhramaStaff_designation = models.CharField("Staff_designation", max_length=100)
   PhramaStaff_photo = models.FileField("Staff_photo", max_length=1000,upload_to='images/')
   PhramaStaff_status=models.CharField("Staff_status",max_length=50,default="")
   Staff_logid=models.ForeignKey(login, on_delete=models.CASCADE, null=True)

class manufactuer(models.Model):
    manufactuer_id=models.AutoField(primary_key=True)
    company_name=models.CharField("company name",max_length=100)
    address=models.CharField("address",max_length=100)
    licence_no=models.CharField("licence no",max_length=100)
    phone_no=models.CharField("phone no",max_length=100)
    login=models.ForeignKey(login,on_delete=models.CASCADE,null=True, related_name='manufacturers')
    status=models.CharField("status",max_length=100)
    
class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_name = models.CharField("Hospital Name", max_length=100)
    license = models.CharField("license Status from Wholesaler", max_length=100)
    status = models.CharField("status", max_length=100)
    hospital_address = models.CharField("hospital_address", max_length=200)
    hospital_phone=models.CharField("hospital_phone",max_length=100)
    login=models.ForeignKey(login,on_delete=models.CASCADE,null=True, related_name='hospital')

class medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=300)
    composition = models.CharField("Composition", max_length=300)
    pharmaceutical_form = models.CharField("Pharmaceutical Form", max_length=300)
    age = models.CharField("Age", max_length=100)
    method_of_administration = models.CharField("Method of Administration", max_length=300)
    contraindications = models.CharField("Contraindications", max_length=500)
    precautions = models.CharField("Precautions", max_length=500)
   

class vaccinerequest(models.Model):
    vaccine_id=models.AutoField(primary_key=True)
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    manufactuer = models.ForeignKey(manufactuer, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    date = models.DateField()
    required_documents = models.FileField(upload_to='manufacture_documents/')
    additional_details = models.TextField()
    stock=models.CharField(max_length=100)
    status=models.CharField("status",max_length=100)

    @property
    def medicine_id(self):
        return self.medicine_id

class distributor(models.Model):
    distributor_id = models.AutoField(primary_key=True)
    distributor_name = models.CharField("Company/Distributor Name", max_length=100)
    address = models.CharField("address", max_length=100)
    license_no= models.CharField("license_no", max_length=100)
    phone=models.CharField("phone",max_length=12)
    status=models.CharField("status",max_length=10)
    login=models.ForeignKey(login,on_delete=models.CASCADE,null=True)

class DistributorAuthorizationRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    distributor = models.ForeignKey(distributor, on_delete=models.CASCADE)
    company_name = models.CharField("Company/Wholesaler Name", max_length=100)
    documents = models.FileField("Documents", upload_to='authorization_documents/')
    status = models.CharField("Status", max_length=100)
    Hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True)
    manufactuer=models.ForeignKey(manufactuer,on_delete=models.CASCADE,null=True)

class BookedVaccineRequest(models.Model):
    vaccinerequest = models.ForeignKey(vaccinerequest, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    distributor = models.ForeignKey('distributor', on_delete=models.CASCADE,null=True)
    date = models.DateField()
    phone_number = models.CharField(max_length=15)
    stock = models.CharField(max_length=100)
    additional_details = models.TextField()
    status = models.CharField(max_length=100, default='booked')

class booked(models.Model):
    booked_id = models.AutoField(primary_key=True)
    Hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE,null=True)
    vaccinerequest=models.ForeignKey(vaccinerequest,on_delete=models.CASCADE,null=True)
    
class expiry(models.Model):
    exp_id=models.AutoField(primary_key=True)
    vaccinerequest=models.ForeignKey(vaccinerequest,on_delete=models.CASCADE,null=True)
    manufactuer=models.ForeignKey(manufactuer,on_delete=models.CASCADE,null=True)
    mfg_date=models.DateField()
    exp_date=models.DateField()




