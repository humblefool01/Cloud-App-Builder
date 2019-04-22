import threading
import subprocess
import os
import time

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.utils.encoding import smart_str
# Create your views here.

from django.http import HttpResponse
#from .models import Question

def index(request):
    #return HttpResponse("Hello, world !")
    return render_to_response('index.html')

def test(request):
    return render_to_response('test.html')


threads = []

exit_status = 0

def onExit2(request, proc):
    global exit_status
    print("*******PROC CALL*******")
    print(proc)
    print(request)
    exit_status = 1   
    print(exit_status) 
    #return redirect('done', permanent=True)
    #return render_to_response('done.html')

def popenAndCall(request, onExit, *popenArgs):
    
    def runInThread(request, onExit, popenArgs):
        proc = subprocess.Popen(list(popenArgs))
        proc.wait()      
        temp = ""          
        onExit(request, onExit2, temp)
        return    
    thread = threading.Thread(target=runInThread, args=(request, onExit, popenArgs))
    threads.append(thread)
    thread.start()
    # returns immediately after the thread starts
    return thread

def onExit(request, onExit2, *popenArgs2):        
    def runInThread2(request, onExit2, popenArgs2):
        path = os.getcwd()
        os.chdir(path + '/myapp/')
        path = os.getcwd()
        os.chdir(path + '/new_cc_project/')
        proc = subprocess.Popen(['./gradlew', 'assembleDebug'])       
        proc.wait()                
        onExit2(request, proc)
        return
    thread = threading.Thread(target=runInThread2, args=(request, onExit2, popenArgs2))
    threads.append(thread)
    thread.start()
    # returns immediately after the thread starts
    return thread
    
def my_python_main_function(request, link):
    popenAndCall(request, onExit, "git", "clone", link, "myapp/new_cc_project")

#link: "https://github.com/codepath/intro_android_demo.git"


def request_page(request):
    global exit_status
    print('This is from python!')
    #if(request.GET.get('mybtn')):            
    link = request.GET.get('mytextbox')
    print('link: ', link)      
    t = my_python_main_function(request, link)
    c = 0
    while exit_status == 0:
        c += 1               
        time.sleep(1)
    return render_to_response('done.html')

def done(request):
    print('Done called')
    #return render_to_response('done.html')
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('app.apk')
    response['X-Sendfile'] = smart_str('/home/kaushik/Documents/Python-Projects/CC_Mini_Project/mysite/myapp/new_cc_project/app/build/outputs/apk')
    return response