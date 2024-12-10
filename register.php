<?php
session_start();
require 'db_connect.php';

$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $pwd = $_POST['password'];
    
    // Verificar si el usuario ya existe
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $exists = $stmt->fetchColumn();

    if ($exists > 0) {
        $message = "El usuario ya existe, elige otro nombre.";
    } else {
        $password = password_hash($pwd, PASSWORD_BCRYPT);
        $stmt = $pdo->prepare("INSERT INTO users (username, password_hash) VALUES (?, ?)");
        $stmt->execute([$username, $password]);
        $message = "Usuario creado con éxito. Ahora puedes iniciar sesión.";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Registro</title>
    <style>
        body { font-family: sans-serif; background: #f0f0f0; }
        .register-container {
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
        .message { color: green; text-align: center; }
    </style>
</head>
<body>
<div class="register-container">
    <h2>Registro</h2>
    <?php if($message) echo "<p class='message'>$message</p>"; ?>
    <form method="post">
        <input type="text" name="username" placeholder="Usuario" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Crear usuario</button>
    </form>
</div>
</body>
</html>
