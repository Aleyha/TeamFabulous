function validateLogin(){

	var user = document.forms["loginForm"]["uname"].value;
	console.log(user);
	var pass = document.forms["loginForm"]["password"].value;
	console.log(pass);
	if(user == "UTAfab" && pass == "password"){
		alert("Access Granted");
		window.location = "stations.html";
		return null;
	}
	else{
		alert("Access Denied");
		return null;
	}

}