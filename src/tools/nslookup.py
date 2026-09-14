import subprocess

# nslookupコマンド
def nslookup(host):
    try:
        result = subprocess.run(["nslookup",host],capture_output=True,text=True)
        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "host":host,
            "success":False,
            "error": str(e)
        }