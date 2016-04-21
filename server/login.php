<?php
//this better fucking work



if(isset($_POST["uname"]) AND isset($_POST["password"])){
	session_start();
	$_SESSION['name'] = $_POST["uname"];
	$_SESSION['pass'] = $_POST["password"];

	if($_SESSION['name'] == 'UTAfab' AND $_SESSION['pass'] == 'password'){
		header('Location:stations.php');
	}
}


?>

<html>
<head>
<title>F.A.R.T. Login</title>
<style>
img{
	position:absolute;
	top:5%;
	left:40%;

}
div.login{
	position:absolute;
	top:35%;
	left:30%;
}
</style>
</head>
<body>
<img src="fablab_image.jpg" alt="Fab Lab UTA" style="position: fixed">
<div class=login>
<form name ="loginForm" method="POST">
	Username:<input type="text" name="uname">
	Password:<input type="password" name="password">
<button type="submit" name="login" value="HTML">Login</button>
</form>

</div>


</body>
</html>