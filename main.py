import os
import time
import hashlib
import ctypes
from datetime import datetime
import sys
import traceback
import threading
import win32serviceutil
import win32service
import win32con
import win32com.client

ctypes.windll.kernel32.SetErrorMode(0x0002)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    try:
        error_msg="".join(traceback.format_exception(exc_type,exc_value,exc_traceback))
        with open(r"C:\Logs\wpn_watcher.log","a",encoding="utf8") as f:
            f.write("\n[CRASH]\n")
            f.write(error_msg)
            f.write("\n")
    except:
        pass
    return

def thread_exception_handler(args):
    sys.excepthook(args.exc_type,args.exc_value,args.exc_traceback)

threading.excepthook=thread_exception_handler
sys.excepthook=global_exception_handler

INTERVAL_SECONDS=2
LOG_PATH=r"C:\Windows\Logs\wpn_watcher.log"
LOG_MAX_SIZE_MB=10

kernel32=ctypes.windll.kernel32
wmi=win32com.client.GetObject("winmgmts:")

os.makedirs(os.path.dirname(LOG_PATH),exist_ok=True)

if os.path.exists(LOG_PATH):
    size_mb=os.path.getsize(LOG_PATH)/(1024*1024)
    if size_mb>LOG_MAX_SIZE_MB:
        os.remove(LOG_PATH)
        with open(LOG_PATH,"w",encoding="utf8") as f:
            msg=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [ENFORCE] Log cleared (exceeded {LOG_MAX_SIZE_MB}MB limit)"
            f.write(msg+"\n")

def write_log(message):
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    line=f"{timestamp} [ENFORCE] {message}"
    with open(LOG_PATH,"a",encoding="utf8") as f:
        f.write(line+"\n")
    print(line)

def relaunch_as_admin():
    params=" ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,params,None,1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_mutex():
    script_path=os.path.abspath(__file__)
    hash_hex=hashlib.sha1(script_path.encode()).hexdigest()
    mutex_name=f"Global\\WatchStopWpn_{hash_hex}"
    handle=kernel32.CreateMutexW(None,True,mutex_name)
    if kernel32.GetLastError()==183:
        return None
    return handle

def get_hosted_services_by_pid(pid):
    services=[]
    try:
        query=f"SELECT Name FROM Win32_Service WHERE ProcessId={pid}"
        for svc in wmi.ExecQuery(query):
            services.append(svc.Name)
    except:
        pass
    return ", ".join(services)

def get_wpn_services():
    services=[]
    try:
        for svc in wmi.ExecQuery("SELECT Name,State,ProcessId FROM Win32_Service"):
            if svc.Name=="WpnService" or svc.Name.startswith("WpnUserService"):
                services.append((svc.Name,svc.State,svc.ProcessId))
    except:
        pass
    return services

def stop_service(name):
    try:
        win32serviceutil.StopService(name)
        write_log(f"STOPPED: {name}")
    except Exception as e:
        write_log(f"FAILED_STOP: {name} Error={str(e)}")

mutex=create_mutex()

if mutex is None:
    write_log("Another instance is already running. Exiting.")
    exit(0)

if not is_admin():
    relaunch_as_admin()
    exit(0)

write_log(f"Watcher started. IntervalSeconds={INTERVAL_SECONDS}")

while True:
    try:
        services=get_wpn_services()
        for name,state,pid in services:
            if state=="Running":
                hosted=""
                if pid:
                    hosted=get_hosted_services_by_pid(pid)
                write_log(f"RUNNING: {name} PID={pid} HostedServices=[{hosted}] Action=STOPPING")
                stop_service(name)
    except Exception as e:
        write_log(f"Loop error: {str(e)}")
    time.sleep(INTERVAL_SECONDS)