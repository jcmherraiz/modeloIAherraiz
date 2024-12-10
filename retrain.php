<?php
session_start();
if(!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit;
}

$pythonPath = "C:\\Users\\José Carlos\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";
$scriptPath = "C:\\xampp\\htdocs\\isolation_forest.py";

$command = "\"$pythonPath\" \"$scriptPath\" --retrain 2>&1";
$output = [];
$return_var = 0;
exec($command, $output, $return_var);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Re-entrenando Isolation Forest</title>
</head>
<body>
<h2>Resultado del re-entrenamiento</h2>
<pre>
<?php
echo "Comando ejecutado: $command\n";
echo "Código de retorno: $return_var\n";
echo "Salida:\n";
print_r($output);
?>
</pre>
<p><a href="admin_panel.php">Volver al Panel</a></p>
</body>
</html>
