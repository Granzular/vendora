window.addEventListener("load",registerEvents,false);

function registerEvents() {
    const csrf = document.querySelector("#csrftoken").value;
    const saveBtn = document.querySelector("#save-profile-btn");

    saveBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const fname = document.querySelector("#id_first_name").value;
        const lname = document.querySelector("#id_last_name").value;
        const username = document.querySelector("#id_username").value;
        const email = document.querySelector("#id_email").value;
        const phone = document.querySelector("#id_phone").value;
        const addr = document.querySelector("#id_delivery_address").value;

        const form = new FormData();
        form.append("first_name", fname);
        form.append("last_name", lname);
        form.append("username", username);
        form.append("email", email);
        form.append("phone", phone);
        form.append("delivery_address", addr);

        fetch("/customers/accounts/profile/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf
            },
            body: form
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Profile update failed");
            }
            return res.text();
        })
        .then((data) => {
            window.location.reload();
            toast("Profile updated");
        })
        .catch((err) => {
            toast("Profile update failed");
            console.error(err);
        });
    });
}