window.addEventListener("load",registerEvents,false);
function registerEvents(e){
    // UPDATE CART COUNT
  fetch("/orders/api/cart/")
    .then((res)=>res.json())
    .then((data)=>{
        let totalCart = data.length;
        updateCartCount(totalCart);
        })
    .catch(err=>console.error(err))
    
     // GETTING ELEMENTS AND ADDING EVENT LISTENERS.
    const add_buttons = document.querySelectorAll(".add-to-cart-btn");
    const remove_buttons = document.querySelectorAll(".remove-from-cart");
    const delete_buttons = document.querySelectorAll(".trash");
    
    [...add_buttons].map((el)=>{el.addEventListener("click",add_to_cart)});
    [...remove_buttons].map((el)=>{el.addEventListener("click",remove_from_cart)});
    [...delete_buttons].map((el)=>{el.addEventListener("click",delete_from_cart)});
    
}

// HELPER FUNCTIONS DEFINITION BLOCK
function syncCartWithServer(){
    let c = localStorage.getItem("cart");
    for (i in c){
        console.log(i.toUpperCase())
        for (j of c[i]){
            console.log("product: ",j.product,"quantity: ",j.quantity);
        }
    }
    let cartData = localStorage.getItem("cart")
    // POST CART
    fetch('/orders/cart_view/', {
  headers: {
    'Content-Type': 'application/json',
      'X-Requested-With':'XMLHttpRequest',
    'X-CSRFToken': document.getElementById('csrftoken').value
  },
        method: "POST",iuii
  body: JSON.stringify(cartData.post)
})
.then(res => res.json())
.then((data) => data)
.catch(err => console.error(err));
    
    // UPDATE CART
    fetch('/orders/cart_view/', {
  headers: {
    'Content-Type': 'application/json',
      'X-Requested-With':'XMLHttpRequest',
    'X-CSRFToken': document.getElementById('csrftoken').value
  },
        method: "UPDATE",
  body: JSON.stringify(cartData.update)
})
.then(res => res.json())
.then((data) => data)
.catch(err => console.error(err));
}

function updateCartCount(totalCart){
    if (totalCart>0){
        let cart_cnt = document.querySelector("#cart-cnt");
        cart_cnt.textContent = totalCart;
        cart_cnt.style.display = "inline-flex";}
}

function getCart(){
    let cart = JSON.parse(localStorage.getItem("cart"));
    if (cart == null){
        cart = {update:[],post:[],cart:[]};
    }
    return cart;
}

function setCart(cart){
    localStorage.setItem("cart",JSON.stringify(cart));
}

function add_to_cart(e){
    console.log(e.target.id);
    const pk = e.target.id;
    let cart = getCart();
    let exist = false;
 for(i of cart.post){
     if (i.product == pk){exist = true}
 }
  if(exist == false){
      cart.post.push({product:pk,quantity:1});
      cart.cart.push({product:pk,quantity:1});
    setCart(cart);
      console.log("Cart added");
      updateCartCount(cart.cart.length);
      //syncCartWithServer();
  }
    
    /*fetch("/orders/api/cart/",{
      headers: {"Content-Type":"application/json",
          "X-CSRFToken":document.querySelector("#csrftoken").value
      },
        method: "POST",
        body:JSON.stringify({product:pk,quantity:1})
  })
    .then(res=>res.json())
    .then(data=>{
        console.log(JSON.stringify(data));
        updateCartCount();
    })
    .catch(err=>console.error(err))*/
    
}
function remove_from_cart(e){
     console.log(e.target.id);
    
}

function delete_from_cart(e){
     
    console.log(e.target.id);
}
