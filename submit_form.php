<?php
if($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $message = $_POST['message'];

    $to = "rodriguez.abrahamdev@gmail.com";
    $subject = "New contact form submission";
    $body = "Name: $name\nEmail: $email\nMessage: $message";

    mail($to, $subject, $body);
}
?>
