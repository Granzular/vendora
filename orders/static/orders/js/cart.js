window.addEventListener("load",registerEvents,false);
function registerEvents(e){
    //localStorage.clear();
    // UPDATE CART UI
  updateCartUI();
    
     // GETTING ELEMENTS AND ADDING EVENT LISTENERS.
    const add_buttons = document.querySelectorAll(".add-to-cart-btn");
    const minus_buttons = document.querySelectorAll(".minus-cartitem-btn");
    const plus_buttons = document.querySelectorAll(".plus-cartitem-btn");
    const delete_buttons = document.querySelectorAll(".trash");
    
    [...add_buttons].map((el)=>{el.addEventListener("click",add_to_cart)});
    [...minus_buttons].map((el)=>{el.addEventListener("click",(e)=>{update_cart(e,"decrease")})});
    [...plus_buttons].map((el)=>{el.addEventListener("click",(e)=>{update_cart(e,"increase")})});
    [...delete_buttons].map((el)=>{el.addEventListener("click",delete_from_cart)});
    
}

// HELPER FUNCTIONS DEFINITION BLOCK

function updateCartUI(e=null){
    
    fetch("/orders/cart_view/",{
      headers: {
          'Content-Type': 'application/json',
          'X-Requested-With':'XMLHttpRequest',
      }}
    )
    .then((res)=>res.json())
    .then((data)=>{
        let totalCart = data.cartCount;
        console.log(JSON.stringify(data))
        let ct = getCart();
        ct.cart = data.cart;
        ct.count = totalCart;
        if (totalCart == 0){
                document.querySelector(".cart-section").innerHTML = `
                <div class="alert alert-warning">
  <strong> Your Cart is currently Empty!</strong>
  <a href="/" class="btn btn-primary-outline">Explore new products</a>
</div>`
            }
        setCart(ct);
        updateCartCount();
        document.querySelector("#cart-total-price").textContent = "₦" + data.totalCartPrice.toLocaleString();
        if (e != null){
            let pk = e.target.id.split("-")[1];
            let priceQ = `#cartitem-price-${pk}`;
            let subTotalQ = `#cart-subtotal-${pk}`;
            for (item of data.cartItems){
                if(item.product==pk){
            document.querySelector(priceQ).textContent = "₦" + item.price.toLocaleString() ;
            document.querySelector(subTotalQ).textContent = "₦" + item.subTotal.toLocaleString();
            }}
        }
        })
    .catch(err=>console.error(err))
}

function syncCartWithServer(e=null){
 
    let cartData = getCart();
    // POST CART
    if (cartData.post.length>0){
    fetch('/orders/api/cart/bulk-create/', {
  headers: {
    'Content-Type': 'application/json',
      'X-Requested-With':'XMLHttpRequest',
    'X-CSRFToken': document.getElementById('csrftoken').value
  },
        method: "POST",
  body: JSON.stringify(cartData.post)
})
.then((res) => {
    if (!res.ok){
        throw new Error(`Http Error: ${res.status}`)
    }
    return res.json()
})
.then((data) => {
    console.log(JSON.stringify(data))
        let cartPost = getCart();
        cartPost.cart = cartPost.cart.concat(data);
        cartPost.post = [];
        console.log("Cart post: ", JSON.stringify(cartPost));
        setCart(cartPost);
    return data;
})
.catch(err => console.error(err));
    }
    // UPDATE CART
    if(cartData.update.length>0){
    console.log("Cart: ",JSON.stringify(cartData))
    fetch('/orders/api/cart/bulk-update/', {
  headers: {
    'Content-Type': 'application/json',
      'X-Requested-With':'XMLHttpRequest',
    'X-CSRFToken': document.getElementById('csrftoken').value
  },
        method: "PATCH",
  body: JSON.stringify(cartData.update)
})
.then((res) => {
    if (!res.ok){
        throw new Error(`Http Error: ${res.status}`)
    }
    return res.json()
})
.then((data) => {
    console.log("DATA: ",JSON.stringify(data))
        let cartUpdate = getCart();
    for(i in data){
 for(j in cartUpdate.cart){
 if(data[i].product == cartUpdate.cart[j].product){
 cartUpdate.cart[j] = data[i];
 break;
}}}
        cartUpdate.update = [];
        console.log("Cart update: ", JSON.stringify(cartUpdate));
        setCart(cartUpdate);
    updateCartUI(e=e);
    return data;
})
.catch(err => console.error(err));
}
    // DELETE CART
    if(cartData.delete.length>0){
    console.log("Cart: ",JSON.stringify(cartData))
    fetch('/orders/api/cart/bulk-delete/', {
  headers: {
    'Content-Type': 'application/json',
      'X-Requested-With':'XMLHttpRequest',
    'X-CSRFToken': document.getElementById('csrftoken').value
  },
        method: "DELETE",
  body: JSON.stringify({"ids":cartData.delete})
})
.then((res) => {
    if (!res.ok){
        throw new Error(`Http Error: ${res.status}`)
    }
    return res.json()
})
.then((data) => {
    console.log("DATA: ",JSON.stringify(data))
        let cart = getCart();
        cart.delete = [];
        console.log("Cart delete: ", JSON.stringify(cart));
        setCart(cart);
    updateCartUI();
    return data;
})
.catch(err => console.error(err));
}
    
}
function updateCartCount(){
    let totalCart = getCart().count;
    let cart_cnt = document.getElementById("cart-cnt");
    if (totalCart>0){
        cart_cnt.textContent = totalCart;
        cart_cnt.style.display = "inline-flex";
    }
    else{
        cart_cnt.style.display = "none";
    }
}

function getCart(){
    let cart = JSON.parse(localStorage.getItem("cart"));
    if (cart == null){
        cart = {delete:[],update:[],post:[],cart:[],count:0};
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
    for(j of cart.cart){
          if (j.product == pk){exist = true}
    }
  if(exist == false){
      cart.post.push({product:pk,quantity:1});
      cart.count += 1;
    setCart(cart);
      console.log("Cart added: ",JSON.stringify(cart));
      updateCartCount();
      syncCartWithServer();
  }
}
function update_cart(e,action){
    
    const pk = e.target.id.split('-')[1];
    let cart = getCart();
    console.log(JSON.stringify(cart));
    let exist = false;
    let cnt = 0;
 for(i of cart.cart){
     if (i.product == pk){exist = true}
 }
    for(j of cart.update){
     if (j.product == pk){cnt += 1}
 }
    
  if(exist == true){
      cart.cart.map((item)=>{
          if (item.product == pk && item.quantity>0 && cnt<1){
              cart.update.push({product:item.product,quantity:item.quantity});
          }
          else{
              return item;
          }
      });
      let del_cart = false;
      cart.update.map((item)=>{
          if (item.product == pk && item.quantity>0){
              if (action=="decrease"){item.quantity -= 1;
                  if(item.quantity == 0){del_cart=true}
              }
              else if(action=="increase"){item.quantity += 1}
              (()=>{
          let q = `#quantity-${pk}`;
          let el = document.querySelector(q);
          el.textContent = item.quantity;
      })();
              return item;
          }
          else{
              return item;
          }
      });
      cart.update.filter((x)=>{if (x!=null){return x}})
    setCart(cart);
      if(del_cart){delete_from_cart(e)}
      syncCartWithServer(e = e);
  }
}

function delete_from_cart(e){
    
    const pk = e.target.id.split('-')[1];
    let cart = getCart();
    let exist = false;
    for(item of cart.cart){
     if (item.product == pk){exist = true;
         cart.delete.push(item.product)
     }
 }
  
 for(i of cart.update){
     if (i.product == pk){exist = true;}
 }
  if(exist == true){
      cart.update = cart.update.filter((item)=>{
          if (item.product != pk ){return item}
      });
      console.log("Cart deleted");
      (()=>{
          document.querySelector("#cart-"+pk).style.display = "none";
      })();
      cart.count = cart.cart.length - cart.delete.length;
      setCart(cart);
      updateCartCount();
      syncCartWithServer();
  }
}

