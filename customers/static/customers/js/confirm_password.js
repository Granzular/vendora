window.addEventListener("load",registerEvents,false);

function registerEvents(e){
	document.getElementsByTagName("input")[1].focus();
	
let password = document.getElementById("id_password");
let confirm_password = document.getElementById("id_confirm_password");
let form = document.getElementById("signup-form");
let error_msg_box = document.getElementById("id_confirm_password_errors");

form.addEventListener('submit',function(e){

	if (password.value.trim() === confirm_password.value.trim()){
		form.submit();
	}
	else{
		e.preventDefault();
		error_msg_box.textContent = "password does not match";
	}

}

);
confirm_password.addEventListener('input',function(e){
console.log("hello")
	if (password.value.trim() === confirm_password.value.trim()){
		error_msg_box.textContent = "";
	}
	else{
		
		error_msg_box.textContent = "password does not match";
	}

}

);
}