<?php
//hello
session_start();
echo "hello";
if(!isset($_SESSION['name'])){
		header('Location:login.php');
}
// if(isset($_POST["station"])){
// $_SESSION['in_use'] = $_POST["station"];
// echo "is this working";
// }
if(isset($_SESSION['in_use'])){
    echo "hello";
    echo "F.A.R.T. already in use!!!";
}
?> 
<html>
<head>
<title>F.A.R.T. Stations</title>
<style>
img{
	position:relative;
	top:5%;
	left:40%;

}
div.direction{
	position:absolute;
	top:40%;
	left:35%;
}

</style>
</head>
<body>
<img src="fablab_image.jpg" alt="Fab Lab UTA" style="position: fixed">
<div class=direction>
<form id=drct action="stations.py" method="post" target="_blank">
	Stations: 
	<input type="text" name="station">
	<input type="submit" value="Submit">
</form>
<h3><a href="logout.php">Click here to log out</a></h3>
<!-- <form id=logout method="GET">
<button name="lgt" type="submit" value="HTML">Logout</button>
</form> -->
<!-- <?php
	
?> -->
</div>
</body>
</html>