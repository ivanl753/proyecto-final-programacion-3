<?php
require 'db.php';
$data = json_decode(file_get_contents('php://input'), true);

$stmt = $pdo->prepare("UPDATE tickets SET estado = ? WHERE id = ?");
$stmt->execute([$data['estado'], $data['id']]);

echo json_encode(['success' => true]);
