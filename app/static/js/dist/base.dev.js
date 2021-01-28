"use strict";

$(function () {
  $(".js-header-responsive").select2({
    width: 'resolve' // need to override the changed default

  });
  var swiper2 = new Swiper('.swiper-container', {
    spaceBetween: 30,
    autoplay: {
      delay: 2000,
      disableOnInteraction: false
    },
    flipEffect: {
      slideShadows: false
    },
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    }
  });
  $(document).on("click", "#closeModal", function () {
    $(".modal-backdrop").removeClass("modal-backdrop fade show ");
    $("#exampleModal").css("opacity", "0");
  });
  $(document).on("click", "#openModal", function () {
    $("#exampleModal").removeClass("none");
    $("<div class='modal-backdrop  show animated fadeIn'></div>").insertAfter("body");
    $("#exampleModal").css("opacity", "1");
  }); // if (!window.location.href.includes("page") || window.location.href.includes("order")|| window.location.href.includes("brand") || window.location.href.includes("sc") || window.location.href.includes("price") || !window.location.href.includes() == "") {
  //   console.log(window.location.href.includes("price"));
  //   $(".pagination .page-item_list:nth-child(3)").addClass("active")
  // }

  $(".children").find("i").remove();
  $('#navbar.navbar-right ul li a').click(function () {
    //clear active status of any parent LI's
    $('#navbar.navbar-right ul li').removeClass('active'); // store id of new active sub-nav

    var currSub = $(this).parent();
    currSub.addClass('active');
    var id = currSub.attr('id'); // clear active status of any sub-nav list

    $('#subnavbar ul.navbar-nav').removeClass('active'); // set selected sub-nav to active

    $('.' + id).addClass('active');
    console.log($('.' + id).attr('class'));
  });
  $(document).on('click', '.tree i', function (e) {
    $(this).parent().siblings('ul').fadeToggle();
    $(this).toggleClass(function () {
      return $(this).is('.fa-angle-right') ? $(this).removeClass("fa-angle-right").addClass("fa-angle-down") : $(this).removeClass("fa-angle-down").addClass("fa-angle-right");
    });
  });
  $(document).on('change', '.tree input[type=checkbox]', function (e) {
    $(this).parent().siblings('ul').find("input[type='checkbox']").prop('checked', this.checked);
    $(this).parentsUntil('.tree').children("input[type='checkbox']").prop('checked', this.checked);
    e.stopPropagation();
  });
  $(".children>ul").hover(function () {
    $(this).css("background-color", "lightgrey").css("border-radius", "0.25em").css("padding", "0 0.5em").css("transition", "0.5s");
  }, function () {
    $(this).css("background-color", "").css("border-radius", "").css("padding", "");
  });
  var myModalEl = document.getElementById('exampleModalCenter'); // myModalEl.addEventListener('hidden.bs.modal', function (event) {
  //   console.log("cerrado");
  //   document.querySelector(".modal-body").innerHTML=""
  // })

  Array.from(document.getElementsByClassName("Details")).forEach(function (element) {
    element.addEventListener("click", function (e) {
      var url = e.target.closest(".Details").getAttribute("tag-url");
      e.target.closest(".Details").classList.add("bg-dark", "is-loading");
      fetch(url).then(function (data) {
        return data.json();
      }).then(function (response) {
        document.querySelector(".modal-body").innerHTML = response.response;
        $('#exampleModalCenter').modal('show');
        e.target.closest(".Details").classList.remove("bg-dark", "is-loading");
      });
    });
  });
  selectProvince = document.getElementById("selectProvince_id");
  selectDistrict = document.getElementById("selectDistrict_id");

  if (selectProvince != null) {
    url = selectProvince.dataset.url;
    fetch(url).then(function (data) {
      return data.json();
    }).then(function (response) {
      selectProvince.disabled = false;

      for (var index = 0; index < response.length; index++) {
        var option = document.createElement("option");
        option.innerText = response[index].fields.name;
        option.setAttribute("value", response[index].pk);
        selectProvince.appendChild(option);
      }
    });
    selectProvince.addEventListener("change", function (e) {
      selectDistrict.disabled = true;
      var id = e.target.options[e.target.options.selectedIndex].attributes[0].value;
      var url = selectProvince.dataset.urldis;
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(id)
      }).then(function (data) {
        return data.json();
      }).then(function (response) {
        selectDistrict.innerHTML = "";
        selectDistrict.disabled = false;
        var selectfirst = document.createElement("option");
        selectfirst.innerText = "Seleccione ditrito...";
        selectDistrict.appendChild(selectfirst);

        for (var index = 0; index < response.length; index++) {
          var option = document.createElement("option");
          option.innerText = response[index].fields.name;
          option.setAttribute("value", response[index].pk);
          selectDistrict.appendChild(option);
        }
      });
    });
  }

  document.getElementById("profile").addEventListener("click", function () {
    window.location.href = this.dataset.url;
  });
  var adresscomponent = document.getElementsByClassName("address_profile");
  Array.from(adresscomponent).forEach(function (element) {
    console.log(element.className);
    element.addEventListener("click", function (e) {
      Array.from(adresscomponent).forEach(function (element2) {
        element2.classList.add("active-adress");

        if (element2.childNodes[2].nextSibling.childNodes[1] != undefined) {
          element2.childNodes[2].nextSibling.removeChild(element2.childNodes[2].nextSibling.childNodes[1]);
        }
      });
      e.target.classList.remove("active-adress");
      var valdir = e.target.childNodes[2].nextElementSibling.className;
      console.log(parseInt(valdir.split("_").pop()));
      console.log(e.target.childNodes[4].nextElementSibling);
    });
  });
});