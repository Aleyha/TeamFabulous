<?php
//hello
session_start();

if(!isset($_SESSION['name'])){
		header('Location:login.php');
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
	position:relative;
	top:40%;
	left:42%;
}

</style>
</head>
<body>
<img src="fablab_image.jpg" alt="Fab Lab UTA" style="position: fixed">
<div class=direction>
<form id=drct action="stations.py" method="post" target="_blank">
	Stations: 
	<select name='dropdown'>
		<option value="Krusty">Krusty</option>
		<option value="Dewey">Dewey</option>
		<option value="Adweeb">Adweeb</option>
		<option value="Khabeir">Khabeir</option>
		<option value="Crayon">Crayon</option>
		<option value="FART">FART</option>
	</select>
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