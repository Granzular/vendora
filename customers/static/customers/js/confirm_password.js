let password = document.getElementById("id_password");
let confirm_password = document.getElementById("id_confirm_password");
let form = document.getElementById("signup_form");
let error_msg_box = document.getElementById("error_msg_box");

form.addEventListener('submit',function(e){

	if (password.value.trim() === confirm_password.value.trim()){
		form.submit();
	}
	else{
		e.preventDefault();
		error_msg_box.innerHTML = "password does not match";
	}

}

);
