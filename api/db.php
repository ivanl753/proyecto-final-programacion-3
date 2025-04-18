<?php
$host = 'sql301.infinityfree.com'; // Cambia esto
$db   = 'if0_38771648_tickets_db'; // Cambia esto
$user = 'if0_38771648';           // Cambia esto
$pass = 'Devsdesign';               // Cambia esto
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

$options = [
  PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
  PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
];

try {
  $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
  echo json_encode(['success' => false, 'error' => $e->getMessage()]);
  exit;
}
?>
