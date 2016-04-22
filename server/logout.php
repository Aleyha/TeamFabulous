<?php
   session_start();
   unset($_SESSION["name"]);
   
   echo 'You have cleaned session';
   header('Location:login.php');
?>