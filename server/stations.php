<?php
// hello
session_start();

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
<meta http-equiv="refresh" content="30;" />
<img src="fablab_image.jpg" alt="Fab Lab UTA" style="position: fixed">
<div class=direction>
<form id=drct action="stations_with_messaging.py" method="post" target="_blank">
	Stations: 
	<input type="text" name="station">
	<input type="submit" value="Submit">
</form>
<h3><a href="logout.php">Click here to log out</a></h3>
<form id=logout method="GET">
<!-- <button name="lgt" type="submit" value="HTML">Logout</button> -->
</form>
<?php
	if(isset($_SESSION['LAST_ACTIVITY']) && (time() - $_SESSION['LAST_ACTIVITY'] > 10)){
	session_unset();
	session_destroy();
	header('Location:login.php');
	?>
		<script>location.reload(true); window.alert("SESSION TIMEOUT"); </script>
	<?php
}
$_SESSION['LAST_ACTIVITY'] = time();
?> 

</div>
</body>
</html>
