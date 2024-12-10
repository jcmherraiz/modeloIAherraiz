<?php
session_start();
require 'db_connect.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $ip = $_SERVER['REMOTE_ADDR'];
    $attempt_time = date('Y-m-d H:i:s');

    // Obtener usuario
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    $status = 'fail';
    $fail_reason = 'User not found or wrong password';

    if ($user && password_verify($password, $user['password_hash'])) {
        $status = 'success';
        $_SESSION['username'] = $username;
    }

    // Insertar el intento
    $stmt = $pdo->prepare("INSERT INTO login_attempts (username, attempt_time, ip_address, status, fail_reason) VALUES (?, ?, ?, ?, ?)");
    $stmt->execute([$username, $attempt_time, $ip, $status, $status=='fail'?$fail_reason:NULL]);
    $attempt_id = $pdo->lastInsertId();

    // Comprobar intentos múltiples fallidos en corto tiempo
    if ($status == 'fail') {
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM login_attempts WHERE ip_address = ? AND attempt_time > (NOW() - INTERVAL 5 MINUTE) AND status='fail'");
        $stmt->execute([$ip]);
        $fail_count = $stmt->fetchColumn();
        if ($fail_count >= 3) {
            $stmt = $pdo->prepare("UPDATE login_attempts SET status='suspicious', fail_reason='Múltiples intentos en corto tiempo' WHERE id = ?");
            $stmt->execute([$attempt_id]);
        }
    }

    // Llamar a isolation_forest para chequear este nuevo intento
    $pythonPath = "C:\\Users\\José Carlos\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";
    $scriptPath = "C:\\xampp\\htdocs\\isolation_forest.py";
    $command = "\"$pythonPath\" \"$scriptPath\" --check_new_attempt $attempt_id 2>&1";
    exec($command, $output, $return_var);

    if ($status === 'success') {
        header("Location: admin_panel.php");
        exit;
    } else {
        $message = "Login failed or suspicious attempt.";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: sans-serif; background: #f0f0f0; }
        .login-container {
            width: 300px; margin: 100px auto; padding: 20px; background: #fff; border-radius: 10px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h2 { text-align: center; }
        form { display: flex; flex-direction: column; }
        input[type="text"], input[type="password"] {
            margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;
        }
        button {
            padding: 10px; border: none; border-radius: 5px; background: #333; color: #fff; cursor: pointer;
        }
        a {
            text-align: center; display:block; margin-top: 10px; color: #333; text-decoration: none;
        }
        a:hover { text-decoration: underline; }
        .message { color: red; text-align: center; }
    </style>
</head>
<body>
<div class="login-container">
    <h2>Login</h2>
    <?php if(isset($message)) echo "<p class='message'>$message</p>"; ?>
    <form method="post">
        <input type="text" name="username" placeholder="Usuario" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Entrar</button>
    </form>
    <a href="register.php">¿No tienes usuario? Regístrate</a>
</div>
</body>
</html>
