"use strict";

x = document.getElementsByClassName("removeItemCart");
var row = document.createElement("div");
row.classList.add("row");
var col = document.createElement("div");
col.classList.add("col-lg-12");
var p = document.createElement("p");
p.classList.add("note", "note-light");
var strong = document.createElement("strong");
strong.textContent = "Nota:";
p.appendChild(strong);
var txt = "Aún no ha agregado productos a su carrito";
strong.after(txt);
col.appendChild(p);
row.appendChild(col);

var _loop = function _loop(i) {
  var element = x[i];
  element.addEventListener("click", function () {
    console.log(this.dataset.url);
    var pinpt = element.closest(".groupInput").firstChild.nextSibling.id;
    var converted = parseInt(pinpt.split("_").pop());
    var data = {
      converted: converted
    }; //    <div class="row">
    //    <div class="col-lg-12"><p class="note note-light">
    //        <strong>Nota:</strong> Aún no ha agregado productos a su carrito
    //      </p></div>print
    //     </div>

    fetch(this.dataset.url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify(data)
    }).then(function (data) {
      return data.json();
    }).then(function (response) {
      document.getElementById("cartCount").innerHTML = response.quantity - response.count;
      document.getElementById("abstractContent").innerHTML = "Subtotal (".concat(response.quantity - response.count, " productos) :");
      element.closest(".cartItem").style.animationPlayState = "running";
      document.getElementById("abstractTotalCart").innerHTML = "S/. ".concat(response.total);
      element.closest(".cartItem").addEventListener("animationend", function () {
        element.closest(".cartItem").remove();
      });
      console.log(document.getElementsByClassName("cartItem").length);

      if (document.getElementsByClassName("cartItem").length == 1) {
        document.getElementById("idContentCart").appendChild(row);
      }
    });
  });
};

for (var i = 0; i < x.length; i++) {
  _loop(i);
}

var selectElement = document.getElementsByClassName('SelectCartCount');
Array.from(selectElement).forEach(function (element) {
  element.addEventListener("change", function (e) {
    var newCount = e.target.value;
    var pinpt = element.closest(".groupInput").firstChild.nextSibling.id;
    var converted = parseInt(pinpt.split("_").pop());
    var data = {
      converted: converted,
      newCount: newCount
    };
    var url = e.target.dataset.url;
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
      return console.log(response);
    });
  });
});