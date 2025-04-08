import winreg
import sys
import os

def register_protocol(protocol_name, script_path):
    key_path = rf"SOFTWARE\Classes\{protocol_name}"
    
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"URL:{protocol_name} Protocol")
            winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

        command_key = key_path + r"\shell\open\command"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
            command = f'"{sys.executable}" "{script_path}" "%1"'
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)

        print(f"Protocol {protocol_name} registered successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    protocol = "savedb"
    script = os.path.join(os.getcwd(), "main.py") 
    register_protocol(protocol, script)
