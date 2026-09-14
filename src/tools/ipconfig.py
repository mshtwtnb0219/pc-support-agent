import subprocess

# ipconfigコマンド実行
def ipconfig():
    try:
        result = subprocess.run(["ipconfig"],capture_output=True,text=True)
        return {
            "success": result.returncode == 0,
            "output": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }