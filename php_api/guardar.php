<?php

header("Content-Type: application/json; charset=UTF-8");

$host = "localhost";
$port = "5432";
$dbname = "ejercicios_python";
$user = "postgres";
$password = "sebas1234";

try {
    $conexion = new PDO(
        "pgsql:host=$host;port=$port;dbname=$dbname",
        $user,
        $password,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ]
    );

    $datos = json_decode(file_get_contents("php://input"), true);

    if (!$datos || !isset($datos["ejercicio"], $datos["entrada"], $datos["resultado"])) {
        http_response_code(400);
        echo json_encode([
            "ok" => false,
            "mensaje" => "Datos incompletos"
        ]);
        exit;
    }

    $sql = "INSERT INTO intentos (ejercicio, entrada, resultado)
            VALUES (:ejercicio, :entrada, :resultado)";

    $sentencia = $conexion->prepare($sql);

    $sentencia->execute([
        ":ejercicio" => $datos["ejercicio"],
        ":entrada" => $datos["entrada"],
        ":resultado" => $datos["resultado"]
    ]);

    echo json_encode([
        "ok" => true,
        "mensaje" => "Guardado correctamente"
    ]);

} catch (PDOException $error) {
    http_response_code(500);

    echo json_encode([
        "ok" => false,
        "mensaje" => "Error de conexión con PostgreSQL",
        "detalle" => $error->getMessage()
    ]);
}
?>
