<?php
require 'db.php';

$stmt = $pdo->query("SELECT * FROM tickets WHERE estado = 'Finalizado'");
echo json_encode($stmt->fetchAll());
