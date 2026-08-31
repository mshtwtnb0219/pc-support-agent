import subprocess

def ping(ip):
    result = subprocess.run(["ping", ip],capture_output=True,text=True)
    return {
        "host": ip,
        "success": result.returncode == 0,
        "output": result.stdout
    }


print(ping("8.8.8.8"))


