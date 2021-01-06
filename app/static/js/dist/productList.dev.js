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
});
document.getElementById("cartEmpty").addEventListener("click", function () {
  fetch(this.dataset.url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    }
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    document.querySelector(".shopping-cart-items").innerHTML = "";
    document.querySelector(".priceTotal").innerHTML = "S/. 0";
    document.getElementById("cartCount").innerHTML = "0";
  });
});

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

function postComment() {
  document.getElementById("postComment").innerHTML = "";
  var form = document.querySelector("#commentForm");
  var dataForm = new FormData(form);
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
}

document.getElementById("openDropdownCart").addEventListener("click", function (e) {
  e.preventDefault();
  var clasarr = document.getElementById("cartContainer").classList;

  if (Array.from(clasarr).indexOf("fadeOut") > -1) {
    document.getElementById("cartContainer").style.display = "block";
    document.getElementById("cartContainer").classList.remove("fadeOut");
    document.getElementById("cartContainer").classList.add("fadeIn");
  } else {
    document.getElementById("cartContainer").classList.add("fadeOut");
    document.getElementById("cartContainer").classList.remove("fadeIn");
  } // if (showDog === true) {
  //   document.getElementById("cartContainer").style.display = "block"
  //   document.getElementById("cartContainer").classList.remove("fadeOut")
  //   document.getElementById("cartContainer").classList.add("fadeIn")
  // } else {
  //   document.getElementById("cartContainer").classList.add("fadeOut")
  //   document.getElementById("cartContainer").classList.remove("fadeIn")
  // }

});
document.addEventListener("click", function (e) {
  var arr = e.target.classList;

  if (Array.from(arr).includes("shopping-cart-header") || Array.from(arr).includes("shopping-cart") || Array.from(arr).includes("btn-danger") || Array.from(arr).includes("shopping-cart-items") || Array.from(arr).includes("cartDrop") || Array.from(arr).includes("shopping-cart-total") || Array.from(arr).includes("priceTotal") || Array.from(arr).includes("goCart") || Array.from(arr).includes("lighter-text") || Array.from(arr).includes("icondrop")) {} else {
    document.getElementById("cartContainer").classList.add("fadeOut");
    document.getElementById("cartContainer").classList.remove("fadeIn");
  }
});
var showDog = false;

function addCartAuth(e) {
  id = parseInt(document.getElementById("productId").value);
  quantity = document.getElementById("quantity").value;
  console.log(id);
  console.log(quantity);
  var data = {
    id: id,
    quantity: quantity
  };
  url = document.getElementById("btnCart").dataset.url;
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
    document.getElementById("cartCount").innerHTML = response.quantity;
  });
}