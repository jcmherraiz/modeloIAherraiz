import sys
import MySQLdb
import MySQLdb.cursors
from sklearn.ensemble import IsolationForest
import numpy as np
import datetime
import joblib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'isoforest_model.pkl')

def ip_to_num(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return 0
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

def status_to_numeric(status):
    map_status = {'success':0, 'fail':1, 'suspicious':2}
    return map_status.get(status, 1)

def get_minutes_of_day(dt_val):
    return dt_val.hour * 60 + dt_val.minute

def retrain(cursor, conn):
    print("[DEBUG] Entrando a la función retrain()...")
    cursor.execute("SELECT * FROM login_attempts")
    data = cursor.fetchall()
    print("[DEBUG] Datos obtenidos de la BD:", len(data), "registros.")

    if len(data) == 0:
        print("[ADVERTENCIA] No hay datos para entrenar el modelo. Modelo no creado.")
        return

    feature_matrix = []
    for row in data:
        ip_num = ip_to_num(row['ip_address'])
        state_val = status_to_numeric(row['status'])
        minutes_of_day = get_minutes_of_day(row['attempt_time'])
        feature_matrix.append([ip_num, minutes_of_day, state_val])

    print("[DEBUG] Longitud de feature_matrix:", len(feature_matrix))
    if len(feature_matrix) == 0:
        print("[ADVERTENCIA] Feature matrix vacía. No se entrena el modelo.")
        return

    print("[DEBUG] Entrenando el Isolation Forest...")
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(feature_matrix)
    joblib.dump(model, model_path)
    print("[DEBUG] Modelo guardado en:", model_path)

def check_new_attempt(cursor, conn, attempt_id):
    print("[DEBUG] Entrando a check_new_attempt con ID:", attempt_id)
    if not os.path.exists(model_path):
        print("[ADVERTENCIA] El modelo no existe. Ejecute --retrain primero.")
        return

    model = joblib.load(model_path)
    cursor.execute("SELECT * FROM login_attempts WHERE id=%s", (attempt_id,))
    row = cursor.fetchone()
    if not row:
        print("[ERROR] No se encontró el intento con ID:", attempt_id)
        return

    ip_num = ip_to_num(row['ip_address'])
    state_val = status_to_numeric(row['status'])
    minutes_of_day = get_minutes_of_day(row['attempt_time'])
    X = [[ip_num, minutes_of_day, state_val]]

    pred = model.predict(X)
    if pred[0] == -1:
        print("[DEBUG] El intento", attempt_id, "fue marcado como sospechoso por el modelo (Isolation Forest).")
        if row['status'] != 'suspicious':
            cursor.execute("UPDATE login_attempts SET status='suspicious', fail_reason='Isolation Forest flagged' WHERE id=%s", (attempt_id,))
            conn.commit()
    else:
        print("[DEBUG] El intento", attempt_id, "no fue marcado como anómalo por el modelo.")

def check_all(cursor, conn):
    print("[DEBUG] Entrando a check_all...")
    if not os.path.exists(model_path):
        print("[ADVERTENCIA] El modelo no existe. Ejecute --retrain primero.")
        return

    model = joblib.load(model_path)
    cursor.execute("SELECT * FROM login_attempts")
    data = cursor.fetchall()
    if len(data) == 0:
        print("[ADVERTENCIA] No hay registros en login_attempts.")
        return

    ids = []
    feature_matrix = []
    for row in data:
        attempt_id = row['id']
        ip_num = ip_to_num(row['ip_address'])
        state_val = status_to_numeric(row['status'])
        minutes_of_day = get_minutes_of_day(row['attempt_time'])
        feature_matrix.append([ip_num, minutes_of_day, state_val])
        ids.append(attempt_id)

    pred = model.predict(feature_matrix)
    anomalos = [ids[i] for i, p in enumerate(pred) if p == -1]

    for attempt_id in anomalos:
        cursor.execute("SELECT status FROM login_attempts WHERE id=%s", (attempt_id,))
        st = cursor.fetchone()['status']
        if st != 'suspicious':
            cursor.execute("UPDATE login_attempts SET status='suspicious', fail_reason='Isolation Forest flagged' WHERE id=%s", (attempt_id,))
    conn.commit()
    print("[DEBUG] Comprobación completa. Anómalos marcados:", len(anomalos))

if __name__ == '__main__':
    print("[DEBUG] Iniciando isolation_forest.py con args:", sys.argv)
    try:
        conn = MySQLdb.connect(
            user='root',
            passwd='',
            host='127.0.0.1',
            db='security_system',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        cursor = conn.cursor()
        print("[DEBUG] Conexión a BD exitosa.")
    except Exception as e:
        print("[ERROR] No se pudo conectar a la base de datos:", e)
        sys.exit(1)

    if '--retrain' in sys.argv:
        retrain(cursor, conn)
    elif '--check_new_attempt' in sys.argv:
        try:
            idx = sys.argv[sys.argv.index('--check_new_attempt')+1]
            check_new_attempt(cursor, conn, idx)
        except IndexError:
            print("[ERROR] Falta el ID después de --check_new_attempt.")
        except ValueError:
            print("[ERROR] ID no válido para --check_new_attempt.")
    elif '--check_all' in sys.argv:
        check_all(cursor, conn)
    else:
        print("[INFO] No se proporcionó argumento (--retrain, --check_new_attempt, --check_all).")

    cursor.close()
    conn.close()
    print("[DEBUG] Finalizando isolation_forest.py.")
