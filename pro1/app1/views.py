from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.db import connection as mydb
from django.contrib.auth.hashers import check_password,make_password
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse

#Mysql Connection
mycursor = mydb.cursor()
#Register function

 


def register(request):
    """
    args:
        request :takes POST request
    return:
        This Function returns admin page on browser
    description:
        This functions takes value from the POST request and checks the password and repassword match.
        If match is true Then it mydb.commit() saves that information in Admins table
    """
    register_q='''insert into Admins
    (Uname,Name,Gender,DOB,Email,Mobileno,Dept,Password) 
    values("%s","%s","%s","%s","%s","%s","%s","%s")'''
    
    if request.method=='POST':
        Password=request.POST['Password']
        Repassword=request.POST['Repassword']
        email=request.POST['Email']
        uname=request.POST['Fname']
        name=request.POST['Lname']
        gender=request.POST['Gender']
        dob=request.POST['DOB']
        mobileno=request.POST['Mobileno']
        dept=request.POST['Dept']

        if Password==Repassword:
            mycursor.execute(register_q%(uname,name,gender,dob,email,mobileno,dept,make_password(Password)))
            mydb.commit()
            return render(request,'app1/register.html',{'info':'Admin registered Succeessfully!!'})

        else:
            return render(request,'app1/register.html',{'info':'Password and repassword should be same'})
    else:
        return render(request,'app1/register.html')





def logIn(request):
    """
    args:
        request :Gets POST Request
        
    return:
        It returns Login page on browser
    description:
        This function gets username and password from the post request and Check for password match in 
        database table if match then it'll give permission to login
    """
    if 'username' not in request.session:

        log_q='select Uname,Name,Password from Admins where Uname="%s"'
        if request.method=='POST':
            uname=request.POST['Fname']
            Pass=request.POST['Password']
            try:
                mycursor.execute(log_q%(uname))
                x=mycursor.fetchall()
            except:
                x=None
            if len(x)!=0:
                if check_password(Pass,x[0][2]):
                    request.session['username']=uname

                    return redirect(show_emp)
                else:
                    return render(request,'app1/login.html',{'Info':'Wrong password'})
            else:
                return render(request,'app1/login.html',{'Info':'UserName Doesent exist'})
        return render(request,'app1/login.html')
    else:
        return redirect(show_emp)





def logout(request):
    request.session['username']
    return redirect(logIn)




def show_emp(request):
    """
    args:
        request :Gets POST request
        uname:Takes usrname from home page through url
    return:
        returns show emp page on browser
    description:
        This function userame through url and check in database for matching data to that username and show 
        on browser
    """
    show_q='select * from employees where Admin_id="%s"'
    if 'username' in request.session:
        uname=request.session['username']
        mycursor.execute(show_q%(uname))
        data=mycursor.fetchall()
        return render(request,'app1/show.html',{'data':data})
    else:
        return redirect(logIn)



def change_pass(request,token):
    """
    args:
        request : Gets POST request
        token: token is a hashed value of email gets through url
    return:
        Returns a password changing page on browser
    description:
        This functions gets token as argument which a hash value of email then on the basis of that token mathcing 
        finds from tha database and then allows to change the password 
    """
    
    change_q='UPDATE Admins SET Password="%s" where email="%s"'
    change_q1='select email,flag from admins where toekn="%s"'


    mycursor.execute(change_q1%(token))
    email=mycursor.fetchone()

    diff=datetime.now()-datetime.strptime(email[1],'%Y-%m-%d %H:%M:%S.%f')
    diff=diff.seconds//60

    if request.method=='POST':
        pass1=request.POST.get('password')
        pass2=request.POST.get('repassword')

        if diff < 1:
            if pass1==pass2:

                pass1=make_password(pass1)
                mycursor.execute(change_q%(pass1,email[0]))
                mydb.commit()
                return render (request,'app1/change_pass.html',{'msg':'Password Has Been Changed'})

            else:
                return render (request,'app1/change_pass.html',{'msg':'Both Password Must Have Same'})

        else:
            return render(request,'app1/change_pass.html',{'msg':'link has been expired'})

    return render (request,'app1/change_pass.html')




def send_mail12_(email):
    """
    args:
        email:this takes email arg from forgot password function
    return:
        reuturn send mail fucntion which is inbuilt of django 
    description:
        This function takes email as args and then change password page link email receiptent etc field pass 
        to the send mail function of django
    """

    send_q='select Email from Admins where Toekn="%s"'

    subject='Your forget password Link'
    message=f'Hi, Click on the link to reset your password  http://127.0.0.1:8000/change_pass/{email}'
    email_from=settings.EMAIL_HOST_USER
    mycursor.execute(send_q%(email))
    val=mycursor.fetchone()[0]
    reciptent_list=[val]
    send_mail(subject,message,email_from,reciptent_list)
    return True


def forgot_pass(request):
    """
    args:
        request :Takes request from url
    return:
        Returns a reset password page on the browser
    description:
        This function takes the email from request and check in db if no  match found it'll show alert
        if match found then it updated token and flag from table and then save it and calls send mail fucntion and
        pass argument that token which is extracted form table 
    """
    forgot_q='select Email,flag from Admins where Email="%s"'
    if request.method=='POST':

        email=request.POST.get('email')
        mycursor.execute(forgot_q%(email))
        x1=mycursor.fetchall()

        if len(x1)==0:
            return render(request,'app1/forgot_pass.html',{'msg':'No userFound with this Username'})

        else:
            userobj=x1[0][0]
            m=make_password(userobj)
            while '/' in m:
                m=make_password(userobj)
            a=datetime.now()
            mycursor.execute('update Admins set Toekn="%s",flag="%s" where Email="%s"'%(m,a,userobj))
            mydb.commit()
            mycursor.execute('select Toekn from Admins where Email="%s"'%(userobj))
            n=mycursor.fetchone()
            send_mail12_(n[0])
        
            return render(request,'app1/forgot_pass.html',{'msg':'Email Has Been Sent'})
    return render(request,'app1/forgot_pass.html')  





def Employee_register(request):
    """
    args:
        request : Gets POST request from url 
        uname:Gets uname from url 
    return:
        return employes register form for that admin who's loggedin
    description:
        This function gets values from post request and save it to table of employees
    """
    
    emp_q='''insert into Employees
    (Uname,Name,Gender,DOB,Emp_Email,Mobileno,Dept,Password,Admin_id) 
    values("%s","%s","%s","%s","%s","%s","%s","%s","%s")'''
    upd_q3='select * from Employees'
    if 'username'  in request.session:
        if request.method=='POST':
            Fname=request.POST['Fname']
            Lname=request.POST['Lname']
            Gender= request.POST['Gender']
            DOB=request.POST['DOB']
            Email=request.POST['Email']
            Mobileno=request.POST['Mobileno']
            Dept=request.POST['Dept']
            Password=request.POST['Password']
            Repassword=request.POST['Repassword']
            admin=request.session['username']

            mycursor.execute('select * from Employees')
            emails=mycursor.fetchall()
            if Password==Repassword:
                for em in emails:
                    print(Email,'________',em[5])
                    if Email==em[5]:
                        messages.warning(request,'Email Id Already Exist')
                        return redirect(show_emp)
                else:
                    Password=make_password(Password)
                    mycursor.execute(emp_q%(Fname,Lname,Gender,DOB,Email,Mobileno,Dept,Password,admin))
                    mydb.commit()
                    messages.success(request,'Employees Record Added Successfully')
                    q='select * from Employees where Admin_id="%s"'
                    mycursor.execute(q%(admin))
                    data=mycursor.fetchall()
                    return JsonResponse({'status':'save','new_data':data})
                        
            else:
                messages.warning(request,'Password And Confirm Password Must Be Match')
                return redirect(show_emp)
        else:
            return redirect(show_emp)
    else:
        return redirect(logIn)





def update_emp(request):
    """
    args:
        id:Gets id from show page of particular candidate
    return:
        return update form for particular candidate who's id is going to pass thrugh url with his information
    description:
        This function gets values from post request and updates in table 
    """
    if 'username'  in request.session:

        upd_q1='select * from Employees where Emp_id="%s"'
        upd_q2='''update Employees set  Uname="%s",Name="%s" ,Gender="%s",
        DOB="%s" ,Emp_Email="%s", Mobileno="%s" ,Dept="%s" where Emp_Id=%d'''
                
        uname=request.session['username']

        if request.method=='POST':
            id=request.POST['id']
            Fname=request.POST['Fname']
            Lname=request.POST['Lname']
            Gender= request.POST['Gender']
            DOB=request.POST['DOB']
            Email=request.POST['Email']
            Mobileno=request.POST['Mobileno']
            Dept=request.POST['Dept']
            admin=request.session['username']
            mycursor.execute(upd_q1%(id))
            form=mycursor.fetchall()
            id=int(id)
            print(id,'__',Fname,'__',Lname,'___',Gender,'___',DOB,'___',Email,'___',Mobileno,'___',Dept)
            # print(emails)
            mycursor.execute(upd_q2%(Fname,Lname,Gender,DOB,Email,Mobileno,Dept,id))
            mydb.commit()
            q='select * from Employees where Admin_id="%s"'
            mycursor.execute(q%(admin))
            data=mycursor.fetchall()
            print(data)
            return JsonResponse({'status':'save','new_data':data})
            
        else:
            return render(request,'app1/show.html')
    else:
        return redirect(logIn)


def del_emp(request):
    """
    args:
        id: Gets id through url from show page
    return:
        deletes the employees of this recieved id
    description:
        This functions deletes the all infotmation of that employee from table who's id going pass in this function 
    """

    del_q='delete from Employees where Emp_id=%d'
    if request.method == 'POST':
        id=request.POST['id']
        if len(id)>0:
            mycursor.execute(del_q%(int(id)))
            mydb.commit()
            admin=request.session['username']
            q='select * from Employees where Admin_id="%s"'
            mycursor.execute(q%(admin))
            data=mycursor.fetchall()
            return JsonResponse({'del_status':1,'new_data':data})
            
    else:
        return redirect(show_emp)
