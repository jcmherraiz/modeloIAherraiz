<?php
session_start();
require 'db_connect.php';

if(!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit;
}

$stmt = $pdo->query("SELECT * FROM login_attempts ORDER BY attempt_time ASC");
$attempts = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head>
<title>Histórico</title>
<style>
    body { font-family: sans-serif; background: #f0f0f0; }
    table { width: 100%; border-collapse: collapse; margin-top:20px; }
    th, td { padding: 10px; border-bottom: 1px solid #ccc; text-align:left; }
    .success { background: #d4edda; }
    .fail { background: #f8d7da; }
    .suspicious { background: #fff3cd; }
    .container { width: 90%; margin: 0 auto; background: #fff; padding:20px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); }
    h2 { text-align:center; }
    .btns { margin:20px 0; text-align:center; }
    .btns a { margin:0 10px; padding:10px 20px; background:#333; color:#fff; text-decoration:none; border-radius:5px; }
</style>
</head>
<body>
<div class="container">
    <h2>Histórico de Intentos</h2>
    <div class="btns">
        <a href="admin_panel.php">Volver al Panel</a>
    </div>
    <table>
        <tr>
            <th>Usuario</th><th>Hora</th><th>IP</th><th>Estado</th><th>Motivo Falla</th>
        </tr>
        <?php foreach($attempts as $att): ?>
            <tr class="<?php echo htmlspecialchars($att['status']); ?>">
                <td><?php echo htmlspecialchars($att['username']); ?></td>
                <td><?php echo htmlspecialchars($att['attempt_time']); ?></td>
                <td><?php echo htmlspecialchars($att['ip_address']); ?></td>
                <td><?php echo htmlspecialchars($att['status']); ?></td>
                <td><?php echo htmlspecialchars($att['fail_reason']); ?></td>
            </tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
