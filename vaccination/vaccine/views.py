from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError
from .models import login as log,Phrama as pstf,manufactuer as manu,distributor as dist,Hospital as hosp
from .models import medicine as med,vaccinerequest as req,DistributorAuthorizationRequest,booked as book,BookedVaccineRequest,expiry
from django.http import HttpResponseBadRequest
from django.db.models import F
from django.contrib import messages
from django.db import transaction 
from django.core.mail import send_mail
from django.contrib.auth.models import User
import requests
import random
import string
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect
import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
import smtplib
from email.mime.text import MIMEText
import csv

# Create your views here.



def index(request):
    try:
        if(request.session["role"] == "admin"):
            return render(request, "adminhead.html",{"msg":"welcome Admin Control pannel"})
        elif (request.session["role"] == "manufacturer"):
            return render(request, "staffhome1.html", {"msg": "welcome  Pharma Control pannel"})
        
        else:
            return render(request, "index.html")
    except:
        return render(request,"index.html",{"msg":""})
    
def Logout(request):
    try:
        del request.session['id']
        del request.session['role']
        del request.session['username']

        response = redirect("/Index")
        return response
    except:
        response = redirect("/Index")
        return response

def Login(request):
    if request.POST:
        user = request.POST["t1"]
        password = request.POST["t2"]
        print("Username and Password:", user, password)

        try:
            data = log.objects.get(username=user, password=password)
            print("Data:", data)
            print("Data Role:", data.role)
            print("User:", data.username)
            print("ID:", data.log_id)

            if data.role == "admin":
                print("Redirecting to adminhead")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.log_id
                response = redirect("/adminhead")
                return response

            elif data.role == "manufacturer":
                print("Redirecting to staffhead")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.log_id
                response = redirect("/staffhead")
                return response

            elif data.role == "distributor":
                print("Redirecting to disthead")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.log_id
                response = redirect("/disthead")
                return response

            elif data.role == "hospital":
                print("Redirecting to hosphead")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.log_id
                response = redirect("/hosphead")
                return response

            else:
                print("Redirecting to Index")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.log_id
                response = redirect("/index")
                
                return response

        except Exception as e:
            print("Exception:", e)
            return render(request, "index.html", {"msg": "invalid user name or password"})

    else:
        return render(request, "index.html", {"msg": ""})
def profile(request):
    msg=""
    if request.POST:
      
        if request.session['role']=="pharma":
          t3 = request.POST["t3"]
          t5 = request.POST["t5"]
          t6 = request.POST["t6"]
          hi = request.POST["hi"]
          pstf.objects.filter(Staff_id=hi).update(PhramaStaff_address=t3,PhramaStaff_phone=t5,PhramaStaff_qualification=t6)
          data = pstf.objects.get(Staff_logid=request.session["id"])
          return render(request, "staff_prof1.html", {"msg": "Profile Updated Successfully", "data": data})
    elif request.session['role']=="pharma":
            data=pstf.objects.get(Staff_logid=request.session["id"])
            return render(request, "staff_prof1.html", {"msg": "", "data": data})            
        
def privacy(request):
    msg=""
    if request.POST:
        t1=request.POST["t1"]
        t2=request.POST["t2"]
        id=request.session["id"]
        data=log.objects.get(log_id=id)
        if data.password==t1:
            msg="sucessfully updated"
            log.objects.filter(log_id=id).update(password=t2)
        else:
            msg="invalid current password"
    returnpage="adminhead.html"
    if request.session["role"] == "hospital":
        returnpage="hosphead.html"
    elif request.session["role"] =="manufacturer":
        returnpage="staffhead.html"
    elif request.session["role"] =="distributor":
        returnpage="staffhead.html"
    return render(request, "privacy.html",{"role":returnpage,"msg":msg})
def AdminHome(request):
    manufacturer_notifications = request.session.get('manufacturer_notifications', 0)
    
    # Reset the notification counter after retrieving it
    request.session['manufacturer_notifications'] = 0
    distributor_notifications = request.session.get('distributor_notifications', 0)
    
    # Reset the notification counter after retrieving it
    request.session['distributor_notifications'] = 0
    return render(request, "adminhome.html", {"new_manufacturer_count": manufacturer_notifications,"new_distributor_count": distributor_notifications})
    
def staffhead(request):
    return render(request,"staffhead.html")

def disthead(request):
    allot_vaccine_request_count = req.objects.filter(status='Assigned').count()
    return render(request, "disthead.html", {'allot_vaccine_request_count': allot_vaccine_request_count})

def hosphead(request):
    allot_vaccine_request_count = req.objects.filter(status='Assigned').count()
    return render(request, "hosphead.html", {'allot_vaccine_request_count': allot_vaccine_request_count})

def list_manu(request):
    data = manu.objects.exclude(status='rejected')
    msg = ""
    return render (request, "list_manu.html",{"b":data,"msg":msg})
def approve_manufacturer(request, manufacturer_id):
    # Fetch the manufacturer object from the database using the manufacturer_id
    manufacturer = manu.objects.get(manufactuer_id=manufacturer_id)
    
    if request.method == 'POST':
        # Update the status to 'approved'
        manufacturer.status = 'approved'
        manufacturer.save()
        
        # Generate random username and password
        
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        login_obj = manufacturer.login
        # Send email to the approved manufacturer with the new login credentials
        send_mail(
            'Your new login credentials',
            f'\nPassword: {new_password}',
            'evotingnew2023@gmail.com',  # Change to your email address
            [login_obj.username],   # Access the email from the login object
            fail_silently=False,
        )
        

        # Update the username and password
       
        login_obj.password = new_password
        login_obj.save()

    # Redirect back to the list_manu page
    return redirect('list_manu')


def reject_manufacturer(request, manufacturer_id):
    # Fetch the manufacturer object from the database using the manufacturer_id
    manufacturer = manu.objects.get(manufactuer_id=manufacturer_id)
    
    # Update the status to 'rejected'
    manufacturer.status = 'rejected'
    manufacturer.save()
    
    # Redirect back to the list_manu page
    return redirect('list_manu')

def list_dist(request):
    data=dist.objects.all()
    msg = ""
    return render (request,"list_dist.html",{"c":data,"msg":msg})

def approve_distributor(request, distributor_id):
        # Fetch the manufacturer object from the database using the manufacturer_id
    distributor = dist.objects.get(distributor_id=distributor_id)
    
    # Update the status to 'approved'
    distributor.status = 'approved'
    distributor.save()
    
    # Redirect back to the list_manu page
    return redirect('list_dist')

def reject_distributor(request, distributor_id):
    # Fetch the manufacturer object from the database using the manufacturer_id
    distributor = dist.objects.get(distributor_id=distributor_id)
    
    # Update the status to 'rejected'
    distributor.status = 'rejected'
    distributor.save()
    
    # Redirect back to the list_manu page
    return redirect('list_dist')

def list_hosp(request):
    data = hosp.objects.all()
    msg = ""
    return render (request, "list_hosp.html",{"c":data,"msg":msg})

def approve_hospital(request, hospital_id):
        # Fetch the manufacturer object from the database using the manufacturer_id
    distributor = hosp.objects.get(hospital_id=hospital_id)
    
    # Update the status to 'approved'
    distributor.status = 'approved'
    distributor.save()
    
    # Redirect back to the list_manu page
    return redirect('list_hosp')

def reject_hospital(request, hospital_id):
    # Fetch the manufacturer object from the database using the manufacturer_id
    distributor = hosp.objects.get(hospital_id=hospital_id)
    
    # Update the status to 'rejected'
    distributor.status = 'rejected'
    distributor.save()
    
    # Redirect back to the list_manu page
    return redirect('list_hosp')

def Add_pharma (request):
    if request.POST:
        t1 = request.POST["t1"]
        t2 = request.POST["t2"]
        t3 = request.POST["t3"]
        t4 = request.POST["t4"]
        t5 = request.POST["t5"]
        t6 = request.POST["t6"]
        t7 = request.POST["t7"]
        t8 = request.FILES["t8"]
        fs = FileSystemStorage()
        fs.save(t8.name, t8)
        # uploaded_file_url = fs.url(filename)
        log.objects.create(username=t4, password=t5, role="pharma");

        data = log.objects.last()
        d = pstf.objects.create(PhramaStaff_name=t1,
                                PhramaStaff_gender=t2,
                                PhramaStaff_address=t3,
                                PhramaStaff_email=t4,
                                PhramaStaff_phone=t5,
                                PhramaStaff_qualification=t6,
                                PhramaStaff_designation=t7,
                                PhramaStaff_photo=t8,
                                PhramaStaff_status="approved",
                                Staff_logid=data,

                                )
        return render(request, "pharma.html", {"msg": "Added sucessfully"})
    else:
        return render(request,"pharma.html",{"msg":""})
def list_pharma(request):

    data=pstf.objects.all()
    msg = ""
    return render(request, "list_pharma.html",{"tutor":data,"msg":msg})

def Add_med(request):
    msg = ""
    if request.method == 'POST':
        # Retrieve data from the form submission
        name = request.POST["name"]
        description = request.POST["description"]
        composition = request.POST["composition"]
        pharmaceutical_form = request.POST["pharmaceutical_form"]
        age = request.POST["age"]
        method_of_administration = request.POST["method_of_administration"]
        contraindications = request.POST["contraindications"]
        precautions = request.POST["precautions"]

        # Create a new 'medicine' object with the provided data
        new_med = med.objects.create(
            name=name,
            description=description,
            composition=composition,
            pharmaceutical_form=pharmaceutical_form,
            age=age,
            method_of_administration=method_of_administration,
            contraindications=contraindications,
            precautions=precautions,
        )

        # Prepare data for the API request
        api_url = 'http://localhost:8080/api/v1/add-vaccine-info'
        api_data = {
            "VaccineID": str(new_med.med_id),  # Assuming med_id is the ID of the newly created medicine
            "VaccineName": name,
            "AgeGroup": age,
            "ContraIndications": contraindications,
            "MethodOfAdministration": method_of_administration,
            "VaccineDescription": description,
            "PharmaceuticalForm": pharmaceutical_form,
            "Precautions": precautions
        }
        print(api_data)
        # Make the API request
        response = requests.post(api_url, json=api_data)

        if response.status_code == 200:
            msg = "Successfully registered and added to blockchain"
        elif response.status_code == 400:
            msg = "Bad Request: Check the data sent to the server"
        else:
            msg = "Failed to make API request: " + str(response.status_code)

    return render(request, "pharma.html", {"msg": msg})

def remove_med(request):
    
    med.objects.filter(med_id=request.GET["id"]).delete()
    response = redirect('/medicine_list/')
    return response

def deletePhrama(request):
    pstf.objects.filter(Staff_id=request.GET["id"]).delete()
    log.objects.filter(log_id=request.GET["log"]).delete()
    response = redirect('/list_pharma/')
    return response

def vaccine_request(request):
    medicines = med.objects.all()
    return render(request, 'vaccine_request.html', {'medicines': medicines})

def vaccine_request_submit(request):
    if request.method == 'POST':
        vaccine_name_id = request.POST['vaccine_name']
        date = request.POST['date']
        required_documents = request.FILES['required_documents']
        additional_details = request.POST['additional_details']
        data1 = manu.objects.get(login=request.session["id"])

        # Get the selected medicine object
        selected_medicine = med.objects.get(pk=vaccine_name_id)

        # Save the vaccine request
        new_request = req(
            medicine=selected_medicine,
            manufactuer=data1,
            vaccine_name=selected_medicine.name,  # Assign the medicine name instead of ID
            date=date,
            required_documents=required_documents,
            additional_details=additional_details,
            stock=0,
            status="waiting"
        )
        new_request.save()

        # Prepare data for the API request
        api_url = 'http://localhost:8080/api/v1/add-manufacture-detail'
        api_data = {
            "VaccineId": str(vaccine_name_id),
            "ManufacturerId": str(data1.manufactuer_id)  # Assuming manufacturer_id is the ID of the manufacturer
        }

        # Make the API request
        response = requests.post(api_url, json=api_data)

        if response.status_code == 200:
            # API request successful
            return redirect('staffhead')  # Redirect to a success page
        else:
            # API request failed
            # Handle the error appropriately
            return redirect('staffhead')  # Redirect to an error page or display a message

    else:
        return redirect('staffhead')

from django.http import JsonResponse

def get_vaccine_details(request):
    if request.method == 'GET' and request.is_ajax():
        vaccine_id = request.GET.get('vaccine_id')
        if vaccine_id:
            vaccine = get_object_or_404(med, pk=vaccine_id)
            vaccine_details = {
                'description': vaccine.description,
                'composition': vaccine.composition,
                # Add other fields as needed
            }
            return JsonResponse(vaccine_details)
        else:
            return JsonResponse({'error': 'Vaccine ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def list_request(request):
    vaccine_requests = req.objects.all()
    return render(request, "list_request.html", {"vaccine_requests": vaccine_requests})

def approve_vaccine_request(request, vaccine_id):
    request_obj = get_object_or_404(req, pk=vaccine_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            request_obj.status = 'approved'
        elif action == 'reject':
            request_obj.status = 'rejected'
        request_obj.save()
    return redirect('list_request')

def reject_vaccine_request(request, vaccine_id):
    request_obj = get_object_or_404(req, pk=vaccine_id)
    request_obj.status = 'rejected'
    request_obj.save()
    return redirect('list_request')

def list_request_manu(request):
    vaccine_requests = req.objects.filter(status="approved")
    return render(request, "list_request_manu.html", {"vaccine_requests": vaccine_requests})

def mark_as_completed(request, medicine_id):
    if request.method == 'POST':
        # Retrieve the vaccine request object using the medicine_id
        vaccine_request = req.objects.get(medicine=medicine_id)
        
        # Get manufacturing and expiry dates from the POST data
        mfg_date = request.POST.get('mfg_date')
        exp_date = request.POST.get('exp_date')

        # Create Expiry object
        xpiry = expiry.objects.create(
            vaccinerequest_id=vaccine_request.vaccine_id,  # Assuming vaccine_id is used as foreign key in expiry model
            mfg_date=mfg_date,
            exp_date=exp_date
        )

        # Update the status to 'completed'
        vaccine_request.status = 'completed'
        vaccine_request.save()
    
        # Prepare data for API request
        api_data = {
            "VaccineId": str(vaccine_request.medicine_id),
            "ManufacturingDate": str(mfg_date),
            "ExpiryDate": str(exp_date)
        }

        # Make a POST request to the API endpoint
        api_url = 'http://localhost:8080/api/v1/add-vaccine-expiry-detail'
        response = requests.post(api_url, json=api_data)
        print(response)

        # Check if the request was successful
        if response.status_code == 200:
            # API call was successful, handle success
            messages.success(request, 'Vaccine manufacturing is completed.')
        else:
            # API call failed, handle error
            # You can log the error or show an error message to the user
            messages.error(request, 'Failed to submit vaccine expiry details. Please try again later.')

    # Redirect to the same page or any desired URL
    return redirect('list_request_manu')



def allot_vaccine_request(request):
    if request.method == 'POST':
        vaccine_request_id = request.POST.get('vaccine_request_id')
        distributor_id = request.POST.get('distributor_id')
        
        print(f"Vaccine Request ID: {vaccine_request_id}, Distributor ID: {distributor_id}")  # Debugging line
        
        if vaccine_request_id and distributor_id:
            try:
                # Use filter instead of get to handle multiple objects
                vaccine_requests = BookedVaccineRequest.objects.filter(vaccinerequest_id=vaccine_request_id)
                distributor = dist.objects.get(distributor_id=distributor_id)
                
                print(f"Vaccine Requests: {vaccine_requests}, Distributor: {distributor}")  # Debugging line
                
                with transaction.atomic():
                    for vaccine_request in vaccine_requests:
                        vaccine_request.status = 'Assigned'
                        vaccine_request.distributor = distributor
                        vaccine_request.save()
                    
                    print("Updated Vaccine Requests")  # Debugging line
                    
            except dist.DoesNotExist as e:
                print(f"Distributor does not exist: {e}")  # Debugging line
                return HttpResponseBadRequest("Invalid distributor ID")
            except BookedVaccineRequest.DoesNotExist as e:
                print(f"Vaccine request does not exist: {e}")  # Debugging line
                return HttpResponseBadRequest("Invalid vaccine request ID")
            distributor_id=str(distributor_id)
            medicine_id = vaccine_requests.first().vaccinerequest.medicine_id
            medicine_id=str(medicine_id)
            # Prepare data for the API request
            api_url = 'http://localhost:8080/api/v1/add-distributor-detail'
            api_data = {
                "VaccineId": str(medicine_id),
                "DistributorId": str(distributor_id)
            }
            print(api_data)
            # Make the API request
            response = requests.post(api_url, json=api_data)

            if response.status_code == 200:
                # API request successful
                return redirect("staffhead")
            else:
                # API request failed
                # Handle the error appropriately
                return HttpResponseServerError("API request failed")
    
    vaccine_requests = BookedVaccineRequest.objects.filter(status='booked')
    distributors = dist.objects.filter(status='approved')
    hospitals = hosp.objects.all()
    
    return render(request, 'allot_vaccine_request.html', {
        'vaccine_requests': vaccine_requests,
        'distributors': distributors,
        'hospitals': hospitals,
    })


def manage_authorization_requests(request):
    if request.method == 'POST':
        distributor_id = dist.objects.get(login=request.session["id"])
        request_id = request.POST.get('request_id')
        status = request.POST.get('status')
        
        if request_id and status:
            authorization_request = BookedVaccineRequest.objects.get(pk=request_id)
            authorization_request.status = "Done"
            authorization_request.save()
            
            return redirect(reverse('manage_authorization_requests'))  # Refresh the page after updating the status
    
    # Fetch all authorization requests
    distributor_id = dist.objects.get(login=request.session["id"])
    authorization_requests = BookedVaccineRequest.objects.filter(distributor_id=distributor_id)
    hospital = hosp.objects.all()
    
    return render(request, 'manage_authorization_requests.html', {'authorization_requests': authorization_requests, 'hospital': hospital})

def adminhead(request):
    manufacturer_notifications = request.session.get('manufacturer_notifications', 0)
    
    # Reset the notification counter after retrieving it
    request.session['manufacturer_notifications'] = 0
    distributor_notifications = request.session.get('distributor_notifications', 0)
    
    # Reset the notification counter after retrieving it
    request.session['distributor_notifications'] = 0
    return render(request, "adminhead.html", {"new_manufacturer_count": manufacturer_notifications,"new_distributor_count": distributor_notifications})

def forgot(request):
    if request.POST:
                s1 = request.POST["t1"]
                
                
                msg="Please Check your Email"
                data=log.objects.get(username=s1)
                ps = data.password


                sub="Forgot Password"
                msg="Please Find Password  : " +ps
                to = s1


                smtp_ssl_host = 'smtp.gmail.com'
                smtp_ssl_port = 465
                # use username or email to log in
                username = 'hokus747@gmail.com'
                password = 'Hokus@123'

                from_addr = 'hokus747@gmail.com'
                to_addrs = [to]

                # the email lib has a lot of templates
                # for different message formats,
                # on our case we will use MIMEText
                # to send only text
                message = MIMEText(msg)
                message['subject'] = sub
                message['from'] = from_addr
                message['to'] = ', '.join(to_addrs)

                # we'll connect using SSL
                server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
                # to interact with the server, first we log in
                # and then we send the message
                server.login(username, password)
                server.sendmail(from_addr, to_addrs, message.as_string())
                server.quit()

                response = redirect('/Index')
                return response
    else:
        return render(request, "forgot.html", {"msg": ""})

def manufacture(request):
    return render(request,"manufactuer.html")
def manufactuer(request):
    msg = ""
    global manufacturer_notifications
    if request.method == 'POST':
        s1 = request.POST["s1"]
        s2 = request.POST["s2"]
        s3 = request.POST["s3"]
        s4 = request.POST["s4"]
        s5 = request.POST["s5"]
        s6 = request.POST["s6"]
        data = log.objects.create(username=s5, password=s6, role="manufacturer")
        manu.objects.create(login=data, company_name=s1, address=s2, licence_no=s3, phone_no=s4,status="waiting")
        
        request.session['manufacturer_notifications'] = request.session.get('manufacturer_notifications', 0) + 1
        
        return render(request, "indexhead.html", {"msg": "Added sucessfully..Wait to admins approval"})
    else:
            msg = "All fields are required."
    return render(request, "manufactuer.html", {"msg": msg})
 
def distributor(request):
    msg=""
    if request.POST:
        a1=request.POST["a1"]
        a2=request.POST["a2"]
        a3=request.POST["a3"]
        a4=request.POST["a4"]
        s5 = request.POST["s5"]
        s6 = request.POST["s6"]
        data = log.objects.create(username=s5, password=s6, role="distributor")
        dist.objects.create(login=data,phone=a4,distributor_name=a1,address=a2,license_no=a3,status="waiting")
        request.session['distributor_notifications'] = request.session.get('distributor_notifications', 0) + 1
        return render(request, "indexhead.html", {"msg": "Added sucessfully..Wait to admins approval"})
    else:
        return render(request,"distributor.html",{"msg":""})
    
def hospital(request):
    msg=""
    if request.POST:
        a1=request.POST["a1"]
        a2=request.POST["a2"]
        a3=request.POST["a3"]
        a4=request.POST["a4"]
        s5 = request.POST["s5"]
        s6 = request.POST["s6"]
        data = log.objects.create(username=s5, password=s6, role="hospital")
        hosp.objects.create(login=data,hospital_phone=a4,hospital_name=a1,license=a2,hospital_address=a3,status="waiting")
        request.session['hospital_notifications'] = request.session.get('hospital_notifications', 0) + 1
        return render(request, "indexhead.html", {"msg": "Added sucessfully..Wait to admins approval"})
    else:
        return render(request,"hospital.html",{"msg":""})

def list_vaccine_requests(request):
    vaccine_requests = req.objects.filter(status="completed")
    vaccine_id = request.GET.get('vaccine_request_id')
    return render(request, 'vaccinerequesthospital.html', {'vaccine_requests': vaccine_requests, 'vaccine_id': vaccine_id})
    

import requests
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect
from django.db import transaction
from datetime import date
from .models import BookedVaccineRequest, Hospital

def book_vaccine_request(request):
    if request.method == 'POST':
        
            vaccine_request_id = request.POST.get('vaccine_request_id')
            hospital_id = hosp.objects.get(login=request.session["id"]).hospital_id  # Get the hospital ID
            stock = request.POST["stock"]
            additional_details = request.POST["additional_details"]
            phone_number = request.POST["phone_number"]
            print("vaccines::",vaccine_request_id)
            print("hosp::",hospital_id)
            if not vaccine_request_id or not hospital_id:
                return HttpResponseBadRequest("Invalid vaccine request or hospital ID")

            
            vaccine_request = req.objects.get(medicine=vaccine_request_id)
            BookedVaccineRequest.objects.filter(status="Done").delete()
            
            with transaction.atomic():
                authorization_request = BookedVaccineRequest.objects.create(
                    vaccinerequest=vaccine_request,
                    date=date.today(),
                    stock=stock,
                    additional_details=additional_details,
                    phone_number=phone_number,
                    status='booked',
                    hospital_id=hospital_id,
                )
                
                vaccine_request.status = 'booked'
                vaccine_request.save()

            # Prepare data for the API request
            api_url = 'http://localhost:8080/api/v1/add-hospital-detail'
            api_data = {
                "VaccineId": str(vaccine_request_id),
                "HospitalId": str(hospital_id)  # Pass the hospital ID as a string
            }

            # Make the API request
            response = requests.post(api_url, json=api_data)

            if response.status_code == 200:
                msg = "Successfully registered and added to blockchain"
            elif response.status_code == 400:
                msg = "Bad Request: Check the data sent to the server"
            else:
                msg = "Failed to make API request: " + str(response.status_code)
    return redirect("list_vaccine_requests")