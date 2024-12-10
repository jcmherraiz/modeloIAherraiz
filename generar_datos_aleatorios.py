import MySQLdb
import MySQLdb.cursors
import random
import datetime
import string

# Configura tu conexión a la base de datos
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'security_system'

NUM_REGISTROS = 50  # Ajusta la cantidad de intentos a insertar

def generar_usuario():
    # Genera un nombre de usuario aleatorio
    chars = string.ascii_lowercase + string.digits
    return "user_" + ''.join(random.choice(chars) for _ in range(5))

def generar_ip():
    # Genera una IP al azar
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generar_status():
    # Mayoría fail o success, algunos suspicious manuales para diversidad
    # Puedes ajustar las probabilidades
    estados = ['success', 'fail', 'fail', 'fail', 'fail', 'fail', 'fail', 'fail', 'fail', 'suspicious']
    return random.choice(estados)

def generar_fail_reason(status):
    if status == 'fail':
        razones = [
            'Contraseña incorrecta',
            'Usuario no existe',
            'Error en el servidor',
            'Sesión expirada',
            'Usuario bloqueado'
        ]
        return random.choice(razones)
    elif status == 'suspicious':
        razones_sospechosas = [
            'Múltiples intentos en corto tiempo',
            'Marcado por IA anómalo',
            'Patrón de comportamiento extraño'
        ]
        return random.choice(razones_sospechosas)
    else:
        return None

def generar_fecha_hora():
    # Genera una fecha y hora aleatoria hoy
    now = datetime.datetime.now()
    # Hora aleatoria dentro del mismo día
    hour = random.randint(0,23)
    minute = random.randint(0,59)
    second = random.randint(0,59)
    fecha_hora = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    return fecha_hora.strftime('%Y-%m-%d %H:%M:%S')

def main():
    try:
        conn = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        cursor = conn.cursor()
        print("[DEBUG] Conexión a la BD exitosa.")
    except Exception as e:
        print("[ERROR] No se pudo conectar a la base de datos:", e)
        return

    for i in range(NUM_REGISTROS):
        username = generar_usuario()
        ip = generar_ip()
        status = generar_status()
        fail_reason = generar_fail_reason(status)
        attempt_time = generar_fecha_hora()

        # Insertar el intento
        sql = """
        INSERT INTO login_attempts (username, attempt_time, ip_address, status, fail_reason)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (username, attempt_time, ip, status, fail_reason))
        conn.commit()
        print(f"[DEBUG] Insertado intento {i+1}: user={username} ip={ip} status={status}")

    cursor.close()
    conn.close()
    print("[INFO] Inserción de datos aleatorios completada. Ahora puedes re-entrenar el modelo.")

if __name__ == '__main__':
    main()
