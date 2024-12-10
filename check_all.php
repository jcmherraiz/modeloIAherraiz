<?php
session_start();
if(!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit;
}

$pythonPath = "C:\\Users\\José Carlos\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";
$scriptPath = "C:\\xampp\\htdocs\\isolation_forest.py";

$command = "\"$pythonPath\" \"$scriptPath\" --check_all 2>&1";
$output = [];
$return_var = 0;
exec($command, $output, $return_var);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Comprobando con IA</title>
</head>
<body>
<h2>Resultado de la comprobación con IA</h2>
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
