from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera
from datetime import datetime
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorator import *
from .speech.GMM1 import *
from .speech.mfeatures import *
from .speech.testrecord import *
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera
import time

from django.http import JsonResponse
# Create your views here.



def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	user = "noura"
	return StreamingHttpResponse(gen(VideoCamera(user)),
					content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
@login_required(login_url='login')
@admin_only
def teacherView(request):
	if(request.method =='GET'):
		module_dir = os.path.dirname(__file__)  
		file_path = os.path.join(module_dir, 'log.txt')   #full path to text.
		data_file = open(file_path , 'r')       
		data = data_file.read()
		print(data)
		context = {'rooms': "helpp"}
	return render(request, 'teacher.html')

def testt(request):
	module_dir = os.path.dirname(__file__)  
	file_path = os.path.join(module_dir, 'log.txt')   #full path to text.
	data_file = open(file_path , 'r')       
	data = data_file.read()
	print(data)
	context = {'rooms': data}
	print(context)
	return JsonResponse(context)


@csrf_exempt
def RecordTrain(request):
    traine(request.user)
    print("sucess")
    return redirect("student")

@csrf_exempt  
def RecordTest(request):
    vari = test()
    print(request.user)
    user_start = vari.find(str(request.user))
    print(user_start)
    if(user_start != -1):
        print("hereeeeeeeeeeeeeeeeeeeee")
        print(os.listdir())
        # os.chdir('./myapp/speech')
        fs = FileSystemStorage(location='D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\development_set\\')
        fs.delete('D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\development_set\\test.wav')
        return redirect('exam')
    else:
        print("unauthenticated")
        return redirect("student")

@csrf_exempt  
@login_required(login_url='login')
def examView(request):
    return render(request, 'exam.html')

@csrf_exempt
def loginView(request):
    if (request.user.is_authenticated):
	    return redirect('verify')
    else:
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if(user is not None):
                print("here")
                login(request, user)
                if(request.user.is_staff):
                    return redirect('teacher')
                else:
                    return redirect('verify')
        else:
            context = {"userID": request.user}
            return render(request, 'login.html', context)



@csrf_exempt
@login_required(login_url='login')
def verifyView(request):
    if(request.method == 'GET'):
        print("get")
        context = {"userID": request.user}
        return render(request, 'verify.html', context)
    else:
        print("here")
        request_file = request.FILES['audio']
        os.chdir('./streamapp/speech')
        
        fs = FileSystemStorage(location="./media/"  )
        #print(request.FILES)
        
        #print("Trueeeee")
        file = fs.save(request_file.name, request_file)
        #fileurl = fs.url(file)
        print("done!!!!")
        #print(fileurl)
        context = {"userID": request.user}
        return render(request, 'verify.html', context)




def logoutUser(request):
	logout(request)
	return redirect('login')




@csrf_exempt
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentView(request):
    context = {"userID": request.user}
    if(request.method == 'GET'):
        print("get")
        
        return render(request, 'student.html', context)
    else:
        print("hereEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        request_file = request.FILES['audio']
        print(os.listdir())

        fs = FileSystemStorage(location='D:\\Users\\noura\\Documents\\GP-CODE\\3django\\AutomatedInvigilator\\Django_VideoStream-master\\streamapp\\speech\\development_set\\')
        print(request.FILES)
        
        print("Trueeeee")
        fs.save(request_file.name, request_file)
        #fileurl = fs.url(file)
        print("done!!!!")
        #print(fileurl)
        return render(request, 'student.html', context)



