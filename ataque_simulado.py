import requests
import time
import random

# URL del formulario de login
LOGIN_URL = "http://localhost/index.php"

# Ajusta según creas conveniente la cantidad de intentos por tipo de ataque
INTENTOS_FUERZA_BRUTA = 10
INTENTOS_DDOS = 20
INTENTOS_SQL_INJECTION = 5

def ataque_fuerza_bruta():
    """
    Simula un ataque de fuerza bruta intentando loguear muchas veces con la misma cuenta
    con contraseñas incorrectas en un corto periodo de tiempo.
    """
    usuario = "admin_test"
    contrasena_incorrecta = "wrongpassword"
    print("[INFO] Iniciando ataque de fuerza bruta...")
    for i in range(INTENTOS_FUERZA_BRUTA):
        data = {
            "username": usuario,
            "password": contrasena_incorrecta
        }
        # Enviar POST al formulario de login
        r = requests.post(LOGIN_URL, data=data)
        print(f"[Fuerza Bruta] Intento {i+1}: {r.status_code}")
        # Pequeño delay para no saturar la máquina local, pero sigue siendo rápido
        time.sleep(0.5)

def ataque_ddos():
    """
    Simula un ataque DDoS enviando múltiples intentos desde diferentes IP simuladas.
    Este es un caso simplificado, dado que requests por defecto no cambia la IP.
    En un entorno real, se necesitaría un proxy o configuración adicional.
    Aquí lo simulamos modificando el User-Agent o un header, o enviando muchos intentos.
    El objetivo es generar un gran número de intentos en poco tiempo.
    """
    print("[INFO] Iniciando ataque DDoS simulado...")
    # Simplemente lanzamos múltiples peticiones muy seguidas con diferentes usuarios aleatorios
    for i in range(INTENTOS_DDOS):
        usuario = "user_ddos_" + str(i)
        contrasena = "password" + str(i)
        data = {
            "username": usuario,
            "password": contrasena
        }
        # Se podrían agregar headers simulando diferentes IP (no real, solo illustrative)
        headers = {
            "X-Forwarded-For": f"192.168.0.{random.randint(1,255)}"
        }
        r = requests.post(LOGIN_URL, data=data, headers=headers)
        print(f"[DDoS] Intento {i+1}: {r.status_code}")
        # Muy poco delay para simular ráfaga
        time.sleep(0.1)

def ataque_inyeccion_sql():
    """
    Simula un ataque con inyección SQL intentando loguear con cadenas sospechosas en el usuario
    o en la contraseña, para ver si el sistema los marca como sospechosos.
    """
    print("[INFO] Iniciando ataque de inyección SQL...")
    # Ejemplo de patrón sospechoso: usuario o pass con ' OR 1=1; --
    for i in range(INTENTOS_SQL_INJECTION):
        # Alternar entre poner la inyección en el usuario o en la contraseña
        if i % 2 == 0:
            usuario = "' OR 1=1;--"
            contrasena = "test"
        else:
            usuario = "sqluser"
            contrasena = "' OR 1=1;--"
        data = {
            "username": usuario,
            "password": contrasena
        }
        r = requests.post(LOGIN_URL, data=data)
        print(f"[SQL Injection] Intento {i+1}: {r.status_code}")
        time.sleep(0.5)

if __name__ == "__main__":
    # Ejecutar los distintos tipos de ataque uno tras otro
    ataque_fuerza_bruta()
    ataque_ddos()
    ataque_inyeccion_sql()
    print("[INFO] Pruebas de ataques finalizadas. Revisa el panel de administración y/o la BD.")
