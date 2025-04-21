<?php
require 'db.php';
require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';
require 'PHPMailer/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;

$data = json_decode(file_get_contents('php://input'), true);

$stmt = $pdo->prepare("SELECT * FROM tickets WHERE id = ?");
$stmt->execute([$data['id']]);
$ticket = $stmt->fetch();

$mail = new PHPMailer(true);
try {
  $mail->isSMTP();
  $mail->Host = 'smtp.gmail.com';
  $mail->SMTPAuth = true;
  $mail->Username = 'i.encarnacion003@gmail.com'; // Cambia esto
  $mail->Password = 'Encarnacion2112';      // Cambia esto
  $mail->SMTPSecure = 'tls';
  $mail->Port = 587;

  $mail->setFrom('i.encarnacion003@gmail.com', 'Sistema de Tickets');
  $mail->addAddress($ticket['Encarnacion2112']);

  $mail->Subject = 'Ticket Finalizado';
  $mail->Body = \"Hola {$ticket['responsable']}, el ticket '{$ticket['titulo']}' ha sido marcado como finalizado.\";

  $mail->send();
  echo json_encode(['success' => true]);
} catch (Exception $e) {
  echo json_encode(['success' => false, 'error' => $mail->ErrorInfo]);
}
