"use strict";

var _this = void 0;

//     const callUrl=async (url)=>{
//       $("#loadingCharge").css("visibility","visible");
//       $("#loadingSpinner").css("visibility","visible");
//           const data=await fetch(url)
//           const dataHtml=await data.text()
//             renderPage(dataHtml,url)      
//           if(renderPage){
//               $("#loadingCharge").css("visibility","hidden");
//               $("#loadingSpinner").css("visibility","hidden");
//           }
//     }
//      const renderPage=(html,url)=>{
//       var parser = new DOMParser();
//       var doc = parser.parseFromString(html, 'text/html');
//       var img = doc.querySelector('.ListProducts');
//       document.getElementById("ListProducts").innerHTML=""
//       document.getElementById("ListProducts").appendChild(img)
//       window.history.pushState({page: "another"}, "another page", url)
//     }
//     const removeParam = (key, sourceURL) => {
//         var rtn = sourceURL.split("?")[0],
//         param,
//         params_arr = [],
//         queryString = sourceURL.indexOf("?") !== -1 ? sourceURL.split("?")[1] : "";
//         if (queryString !== "") {
//         params_arr = queryString.split("&");
//         for (var i = params_arr.length - 1; i >= 0; i -= 1) {
//             param = params_arr[i].split("=")[0];
//             if (param === key) params_arr.splice(i, 1);    
//         }
//         rtn = rtn + "?" + params_arr.join("&");
//         }
//         return rtn.replace(/%2C/g, ",");
//     };
// document.querySelectorAll(".marca") .forEach(element => {
//     element.addEventListener("click",function(){
//         oldURL = window.location.href;
//         var url = new URL(oldURL);
//         url.searchParams.set("brand",element.value); // setting your param
//         var newUrl = url.href;
//         newUrl2 = removeParam("page", newUrl);
//         callUrl(newUrl2.replace(/%2C/g, ","))
//     })
// });
var a = 0;
Array.from(document.getElementsByClassName("subcatCheck")).forEach(function (element) {
  var inp = element.closest(".tree").querySelector("input");
  Array.from(inp).forEach(function (element2) {
    if (element2.getAttribute("checked")) {
      element2.setAttribute("checked", _this.checked);
      document.getElementById("cleanCheckFilter").setAttribute("disabled", false);
    }
  });
});
Array.from(document.getElementsByClassName("custom-control-input")).forEach(function (element) {
  if (element.getAttribute("checked")) {
    document.getElementById("cleanFilter").setAttribute("disabled", false);
  }
}); // document.getElementById("cartEmpty").addEventListener("click", function () {
//   fetch(this.dataset.url, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrftoken
//     }
//   }).then(response => response.json()).then(data => {
//     document.querySelector(".shopping-cart-items").innerHTML = ""
//     document.querySelector(".priceTotal").innerHTML = "S/. 0"
//     document.getElementById("cartCount").innerHTML = "0"
//   })
// })

var addCart = function addCart(url) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    }
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    console.log(data.data);
    document.querySelector(".shopping-cart-items").innerHTML = "";
    document.querySelector(".priceTotal").innerHTML = "";
    document.getElementById("cartCount").innerHTML = "";

    for (var _i = 0, _Object$keys = Object.keys(data.data); _i < _Object$keys.length; _i++) {
      var key = _Object$keys[_i];
      var li = document.createElement("li");
      var img = document.createElement("img");
      var spanName = document.createElement("span");
      spanName.classList.add("item-name");
      spanName.innerHTML = data.data[key].name;
      var spanPrice = document.createElement("span");
      spanPrice.classList.add("item-price");
      spanPrice.innerHTML = "S/. " + data.data[key].price;
      var spanCant = document.createElement("span");
      spanCant.classList.add("item-quantity");
      spanCant.innerHTML = "Cantidad:" + data.data[key].quantity;
      img.setAttribute("src", "/media/" + data.data[key].image);
      li.classList.add("clearfix");
      li.append(img);
      li.append(spanName);
      li.append(spanPrice);
      li.append(spanCant);
      document.querySelector(".shopping-cart-items").append(li);
    }

    document.querySelector(".priceTotal").innerHTML = "S/. " + data.total;
    document.getElementById("cartCount").innerHTML = data.cantidad;
  });
};

function addCartAuth(e) {
  id = parseInt(document.getElementById("productId").value);
  quantity = document.getElementById("quantity").value;
  document.getElementById("AddCart").disabled = true;
  console.log(parseInt(quantity));
  var data = {
    id: id,
    quantity: quantity
  };
  url = document.getElementById("AddCart").dataset.url;
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify(data)
  }).then(function (data) {
    return data.json();
  }).then(function (response) {
    console.log(response);
    document.getElementById("quantity").value = "";
    document.getElementById("cartCount").innerHTML = response.quantity + parseInt(document.getElementById("cartCount").innerHTML);
    document.getElementById("AddCart").textContent = "Agregado";
    document.getElementById("AddCart").disabled = false;
    document.querySelector(".priceTotal").innerHTML = "S/. ".concat(response.total);
  });
}

function postComment() {
  document.getElementById("postComment").innerHTML = "";
  var form = document.querySelector("#commentForm");
  var dataForm = new FormData(form);
  console.log(dataForm);
  var parent = document.createElement("div");
  var loader = document.createElement("span");
  loader.style.marginRight = "2px";
  loader.classList.add("spinner-border", "spinner-border-sm");
  loader.setAttribute("role", "status");
  loader.setAttribute("aria-hidden", "true");
  parent.appendChild(loader);
  loader.after("Publicando...");
  console.log(parent);
  document.getElementById("postComment").appendChild(parent);
  document.getElementById("postComment").disabled = true;
  fetch(form.getAttribute("action"), {
    method: "POST",
    body: dataForm
  }).then(function () {
    document.getElementById("postComment").innerHTML = "";
    document.getElementById("postComment").textContent = "Publicado";
    document.getElementById("postComment").disabled = false;
  });
} // let openDropdownCart=document.getElementById("openDropdownCart")
// if(openDropdownCart!=null){
// openDropdownCart.addEventListener("click", (e) => {
//   e.preventDefault()
//   let clasarr = document.getElementById("cartContainer").classList
//   if (Array.from(clasarr).indexOf("fadeOut") > -1) {
//     document.getElementById("cartContainer").style.display = "block"
//     document.getElementById("cartContainer").classList.remove("fadeOut")
//     document.getElementById("cartContainer").classList.add("fadeIn")
//   } else {
//     document.getElementById("cartContainer").classList.add("fadeOut")
//     document.getElementById("cartContainer").classList.remove("fadeIn")
//   }
//   if (showDog === true) {
//     document.getElementById("cartContainer").style.display = "block"
//     document.getElementById("cartContainer").classList.remove("fadeOut")
//     document.getElementById("cartContainer").classList.add("fadeIn")
//   } else {
//     document.getElementById("cartContainer").classList.add("fadeOut")
//     document.getElementById("cartContainer").classList.remove("fadeIn")
//   }
// })}


document.addEventListener("click", function (e) {
  var arr = e.target.classList;

  if (Array.from(arr).includes("shopping-cart-header") || Array.from(arr).includes("shopping-cart") || Array.from(arr).includes("btn-danger") || Array.from(arr).includes("shopping-cart-items") || Array.from(arr).includes("cartDrop") || Array.from(arr).includes("shopping-cart-total") || Array.from(arr).includes("priceTotal") || Array.from(arr).includes("goCart") || Array.from(arr).includes("lighter-text") || Array.from(arr).includes("icondrop")) {} else {
    document.getElementById("cartContainer").classList.add("fadeOut");
    document.getElementById("cartContainer").classList.remove("fadeIn");
  }
});
var showDog = false;

function cleanAddress() {
  document.getElementById("method_address").value = "post";
  document.getElementById("address_profile").value = "";
  document.getElementById("description_id").setAttribute("value", "");
  document.getElementById("description_id").classList.remove("active");
  document.getElementById("refrences_id").setAttribute("value", "");
  document.getElementById("refrences_id").classList.remove("active");
  document.getElementById("selectProvince_id").value = 0;
  document.getElementById("selectDistrict_id").value = 0;
  var adresscomponent = document.getElementsByClassName("address_profile");
  Array.from(adresscomponent).forEach(function (element) {
    element.classList.remove("active-adress");
  });
}

function createAddress() {
  var form = document.querySelector("#formAddress");
  var formData = new FormData(form);
  fetch(form.getAttribute("action"), {
    method: "POST",
    body: formData
  }).then(function (data) {
    return data.json();
  }).then(function (response) {
    console.log(response);
    var grid = document.createElement("div");
    grid.classList.add("grid", "address-component", "grid-c-10", "grid-r-1-1-4");
    var txt1 = document.createTextNode("");
    var i = document.createElement("i");
    i.textContent;
    i.classList.add("align-self-center", "justify-self-center", "fas", "fa-map-marker-alt");
    var txt2 = document.createTextNode("");
    var pnamePro = document.createElement("p");
    var namePro = document.createElement("strong");
    namePro.textContent = response.province;
    pnamePro.classList.add("address_" + response.id, "justify-content-between", "d-flex");
    pnamePro.appendChild(namePro);
    var txt3 = document.createTextNode("");
    var pnameDis = document.createElement("p");
    var nameDis = document.createElement("strong");
    nameDis.textContent = response.district;
    pnameDis.classList.add("grid-row-start-2", "grid-column-start-2");
    pnameDis.appendChild(nameDis);
    var txt4 = document.createTextNode("");
    var pnameDes = document.createElement("p");
    pnameDes.textContent = response.description;
    pnameDes.classList.add("grid-row-start-3", "grid-column-start-2");
    var txt5 = document.createTextNode("");
    var pnameRef = document.createElement("p");
    pnameRef.style.fontSize = "0.8em";
    pnameRef.textContent = "Ref: " + response.refrences;
    pnameRef.classList.add("grid-row-start-4", "grid-column-start-2");
    var txt6 = document.createTextNode("");
    grid.appendChild(txt1);
    grid.appendChild(i);
    grid.appendChild(txt2);
    grid.appendChild(pnamePro);
    grid.appendChild(txt3);
    grid.appendChild(pnameDis);
    grid.appendChild(txt4);
    grid.appendChild(pnameDes);
    grid.appendChild(txt5);
    grid.appendChild(pnameRef);
    grid.appendChild(txt6);
    document.querySelector(".form_Address").classList.add("none");
    document.getElementById("grid_adress_container").insertBefore(grid, document.getElementById("add_adress_circle"));
    var adresscomponent = document.getElementsByClassName("address-component");
    Array.from(adresscomponent).forEach(function (element) {
      console.log(element);
      element.addEventListener("click", function (e) {
        console.log(e.target.childNodes);
        Array.from(adresscomponent).forEach(function (element2) {
          element2.classList.add("active-adress");

          if (element2.childNodes[2].nextSibling.childNodes[1] != undefined) {
            element2.childNodes[2].nextSibling.removeChild(element2.childNodes[2].nextSibling.childNodes[1]);
          }
        });
        e.target.classList.remove("active-adress");
        var valdir = e.target.childNodes[2].nextElementSibling.className;
        document.getElementById("address").value = parseInt(valdir.split("_").pop());
        var img = document.createElement("img");
        img.src = "/static/icons/comprobado.png";
        e.target.childNodes[2].nextElementSibling.appendChild(img);
      });
    });
  });
}