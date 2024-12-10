import requests
import time
import random
import string

LOGIN_URL = "http://localhost/proyecto/index.php"

# Cantidades de intentos
INTENTOS_NORMALES = 10
INTENTOS_ANOMALOS = 5

def generar_usuario_anomalo():
    # Genera un usuario con caracteres raros y mezcla de mayúsculas, minúsculas, dígitos y símbolos
    chars = string.ascii_letters + string.digits + "#@!$%&"
    return ''.join(random.choice(chars) for _ in range(12))

def generar_contrasena_anomala():
    # Contraseña muy larga y rara
    chars = string.ascii_letters + string.digits + "#@!$%&"
    return ''.join(random.choice(chars) for _ in range(20))

def intentos_normales():
    print("[INFO] Generando intentos normales...")
    usuarios_normales = ["usuario_normal_1", "usuario_normal_2"]
    ips_normales = ["192.168.0.10", "192.168.0.11"]
    for i in range(INTENTOS_NORMALES):
        usuario = random.choice(usuarios_normales)
        contrasena = "password_normal"
        # No todos fallan, algunos pueden ser éxitos si existe ese usuario (depende de tu sistema)
        # Si no existen, igual se registran como fallos "normales"
        headers = {
            "X-Forwarded-For": random.choice(ips_normales)
        }
        data = {
            "username": usuario,
            "password": contrasena
        }
        r = requests.post(LOGIN_URL, data=data, headers=headers)
        print(f"[Normal] Intento {i+1}: {r.status_code} (usuario={usuario})")
        # Espera 30 segundos entre intentos normales
        time.sleep(30)

def intentos_anomalos_sutiles():
    print("[INFO] Generando intentos anómalos sutiles...")
    ips_anas = ["10.250.99.77", "10.250.100.200"]
    for i in range(INTENTOS_ANOMALOS):
        usuario = generar_usuario_anomalo()
        contrasena = generar_contrasena_anomala()
        headers = {
            "X-Forwarded-For": random.choice(ips_anas)
        }
        data = {
            "username": usuario,
            "password": contrasena
        }
        r = requests.post(LOGIN_URL, data=data, headers=headers)
        print(f"[Anómalo] Intento {i+1}: {r.status_code} (usuario={usuario})")
        # Espera 90 segundos para no disparar la detección por múltiples intentos en corto tiempo
        time.sleep(90)

if __name__ == "__main__":
    # Primero generar algunas muestras normales
    intentos_normales()

    # Luego algunos intentos anómalos intercalados
    # Podrías volver a generar intentos normales después de algunos anómalos, por más realismo
    intentos_anomalos_sutiles()

    # Generar de nuevo algunos intentos normales para "disfrazar" los anómalos
    intentos_normales()

    print("[INFO] Ataques sutiles finalizados. Ahora re-entrena el modelo y revisa el panel.")
