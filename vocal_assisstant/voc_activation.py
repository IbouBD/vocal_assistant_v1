import keyboard
import subprocess

SCRIPT_PATH = "C:/project/vocal_assisstant/voc_assistant.py"

def on_f7(e):
    print("Exécution du script")
    
    try:
        output = subprocess.run(["python", SCRIPT_PATH], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur d'exécution:", e)
        print("Sortie d'erreur:", e.stderr)
    except Exception as e:
        print("Erreur inattendue:", e)
    else:
        print(output.stdout)

keyboard.on_press_key("f7", on_f7)

keyboard.wait("esc")