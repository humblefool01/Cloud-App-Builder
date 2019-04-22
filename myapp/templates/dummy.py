import threading
import subprocess
import os

def popenAndCall(onExit, *popenArgs):
    
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(list(popenArgs))
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread

def onExit():
    os.chdir(os.path.abspath(os.path.expanduser('cc_project')))
    #subprocess.check_call('pwd')
    #subprocess.check_call(['./gradlew', 'assembleDebug'])

popenAndCall(onExit, "git", "clone", "https://github.com/codepath/intro_android_demo.git", "cc_project")