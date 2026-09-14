import subprocess

# pingコマンド実行
def ping(ip):
    try:
        result = subprocess.run(["ping", ip],capture_output=True,text=True, timeout=10)
        return {
            "host": ip,
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "host": ip,
            "success":False,
            "error": str(e)
        }
        
    