<?php
require 'db.php';

$stmt = $pdo->query("SELECT * FROM tickets WHERE estado != 'Finalizado' ORDER BY id DESC");
echo json_encode($stmt->fetchAll());
