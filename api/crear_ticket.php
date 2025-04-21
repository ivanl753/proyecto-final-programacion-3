<?php
require 'db.php';
$data = json_decode(file_get_contents('php://input'), true);

$stmt = $pdo->prepare("INSERT INTO tickets (titulo, descripcion, responsable, correo_responsable, prioridad) VALUES (?, ?, ?, ?, ?)");
$stmt->execute([
  $data['titulo'], $data['descripcion'], $data['responsable'], $data['correo'], $data['prioridad']
]);

echo json_encode(['success' => true]);
