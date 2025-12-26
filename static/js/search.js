window.addEventListener("load",registerEvents,false);

function registerEvents(e){
    // assign variables for elements
    const searchBox = document.querySelector("#search-box");
    const searchIcon = document.querySelector("#search-icon");
    const searchResult = document.querySelector("#search-result-section");
    const searchResultCont = document.querySelector("#search-result-section-cont");
    searchBox.addEventListener("click",(e)=>{searchResultCont.style.display ="block";
        document.querySelector("#close-search-btn").addEventListener("click",(e)=>{searchResultCont.style.display="none";});
    });
    searchIcon.addEventListener("click",handleSearch,false);
    
searchBox.addEventListener("keydown",(e)=>{
    if (e.key == "Enter"){
    handleSearch(e)}},false);
    
    function updateSearchBoxPlaceholder(index){
        if (index>2){index=0}
        let phraseList =["search for a product","search categories","find love"];
        searchBox.setAttribute("placeholder",phraseList[index]);
        return setTimeout(updateSearchBoxPlaceholder,4000,index+1)
    }
    updateSearchBoxPlaceholder(0)
}


function handleSearch (e){
    // assign variables
    const filterParam = document.querySelector("#filter").value;
    const searchBox = document.querySelector("#search-box");
    const searchResult = document.querySelector("#search-result-section");
    const searchResultCont = document.querySelector("#search-result-section-cont");
        // start of function
    const word = searchBox.value;
    // build url 
    const url = `/products/search/?q=${word}&filter=${filterParam}`;
    // make request 
    fetch(url)
    .then(res=>res.json())
    .then((data)=>{
        console.log(JSON.stringify(data).slice(0,100));
        let temp = "";
        if (data.result.empty){
            temp += `<div class="search-result-item">${data.result.empty}</div>`;
        }
        else{
            for(item of data.result){
                temp += `
                <div class='search-result-item'><a href='${item.url}'>${item.name}</a></div>`;
            }
        }
        searchResult.innerHTML = temp;
        searchResult.style.display = "block";
        searchResultCont.style.display = "block";
        document.querySelector("#close-search-btn").addEventListener("click",(e)=>{
            searchResult.style.display="none";
            searchResultCont.style.display="none";
        });
        return data;
    })
    .catch(err=>console.log(err))
    } // end of  function

