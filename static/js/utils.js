/* These script contains general utility functions; includes logic for components */

function toast(msg){
    // this is an alternative to the js alert and bootstrap modal
    const modal = `
    <div class="modal-head">vendora sentry
    <button class="modal-close-btn">close</button>
    </div>
    <div class="modal-body">
    <p class="modal-text">${msg}</p>
    </div>
    `;
    let modalCont = document.createElement("div");
    modalCont.setAttribute("class","modal");
    modalCont.innerHTML = modal;
    document.body.append(modalCont);
    modalCont.querySelector(".modal-close-btn").addEventListener("click",(e)=>{
        modalCont.remove();
    });
}