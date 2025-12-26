/* The urls used in this are hardcoded, update regularly.
 * */
const ADMIN_PRODUCT_URL = "/myadmin/dashboard/product/";
const ADMIN_INVENTORY_URL = "/myadmin/dashboard/inventory/";
const ADMIN_CATEGORY_URL = "/myadmin/dashboard/category/";


window.addEventListener("load",register,false);

function inventoryCard(e){
    const btnManage = document.querySelector("#manage-inventory-btn");
    btnManage.addEventListener("click",(e)=>{window.location.href = ADMIN_INVENTORY_URL},false);
}

function productCard(e){
    const btnManage = document.querySelector("#manage-product-btn");
    btnManage.addEventListener("click",(e)=>{window.location.href = ADMIN_PRODUCT_URL},false);
}

function categoryCard(e){
    const btnManage = document.querySelector("#manage-category-btn");
    btnManage.addEventListener("click",(e)=>{window.location.href = ADMIN_CATEGORY_URL},false);
}

function register(e){
    
    inventoryCard();
    productCard();
    categoryCard();
}

