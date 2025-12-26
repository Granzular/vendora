window.addEventListener("load",registerEvents);

function set_active_link(){
    /* Only works properly for a multipage website; if the links are on the same page, unwanted behaviours. shall be updated.*/
    const nav_links = document.querySelectorAll(".nav-link");
    for(i of nav_links){
        if(i.href === window.location.href){
            
            i.classList.add("active-link");
        }
        else{
            i.classList.remove("active-link");
        }
    }
    }

function registerEvents(e){
    set_active_link();
    const nav_links = document.querySelectorAll(".nav-link");
    const nav_icon = document.querySelector(".menuicon");
    const navbar_ul = document.querySelector(".navbar ul"); 
    nav_icon.addEventListener("click",toggle_navbar);
    
    function  toggle_navbar(e){
        
       if( navbar_ul.style.display == "block"){
           navbar_ul.style.display = "none";
           document.querySelector(".menuicon").src = "/media/images/menuicon01.png";
           
       }
        else{
            navbar_ul.style.display = "block";
            document.querySelector(".menuicon").src = "/media/images/close.png";
        }
    }
    
}
    
