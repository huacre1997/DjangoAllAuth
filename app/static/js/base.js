$(function () {
  $(".js-header-responsive").select2({
    width: 'resolve' // need to override the changed default
  });

  var swiper3 = new Swiper('.swiper-index', {
    spaceBetween: 30,
    autoplay: {
      delay: 2000,
      disableOnInteraction: false,
    },
    flipEffect: {
      slideShadows: false,
    },
    loop: true,

    pagination: {
      el: '.swiper-pagination-index',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });

  $(document).on("click", "#closeModal", function () {
    $(".modal-backdrop").removeClass("modal-backdrop fade show ")
    $("#exampleModal").css("opacity", "0")
  });
  $(document).on("click", "#openModal", function () {
    $("#exampleModal").removeClass("none")

    $("<div class='modal-backdrop  show animated fadeIn'></div>").insertAfter("body");
    $("#exampleModal").css("opacity", "1")
  });
  // if (!window.location.href.includes("page") || window.location.href.includes("order")|| window.location.href.includes("brand") || window.location.href.includes("sc") || window.location.href.includes("price") || !window.location.href.includes() == "") {
  //   console.log(window.location.href.includes("price"));
  //   $(".pagination .page-item_list:nth-child(3)").addClass("active")
  // }
  $(".children").find("i").remove()
  $('#navbar.navbar-right ul li a').click(function () {
    //clear active status of any parent LI's
    $('#navbar.navbar-right ul li').removeClass('active');

    // store id of new active sub-nav
    var currSub = $(this).parent();
    currSub.addClass('active')
    var id = currSub.attr('id');

    // clear active status of any sub-nav list
    $('#subnavbar ul.navbar-nav').removeClass('active');

    // set selected sub-nav to active
    $('.' + id).addClass('active');

    console.log($('.' + id).attr('class'));

  });

  $(document).on('click', '.tree i', function (e) {
    $(this).parent().siblings('ul').fadeToggle();
    $(this).toggleClass(function () {
      return $(this).is('.fa-angle-right') ? ($(this).removeClass("fa-angle-right").addClass("fa-angle-down")) : ($(this).removeClass("fa-angle-down").addClass("fa-angle-right"));

    })

  });
  $(document).on('change', '.tree input[type=checkbox]', function (e) {

    $(this).parent().siblings('ul').find("input[type='checkbox']").prop('checked', this.checked);
    $(this).parentsUntil('.tree').children("input[type='checkbox']").prop('checked', this.checked);
    e.stopPropagation();
  });
  $(".children>ul").hover(function () {
    $(this).css("background-color", "lightgrey").css("border-radius", "0.25em").css("padding", "0 0.5em").css("transition", "0.5s")

  }, function () {
    $(this).css("background-color", "").css("border-radius", "").css("padding", "")

  });
  var myModalEl = document.getElementById('exampleModalCenter')
  // myModalEl.addEventListener('hidden.bs.modal', function (event) {
  //   console.log("cerrado");
  //   document.querySelector(".modal-body").innerHTML=""

  // })
  Array.from(document.getElementsByClassName("Details")).forEach((element) => {

    element.addEventListener("click", function (e) {
      let url = e.target.closest(".Details").getAttribute("tag-url")
      e.target.closest(".Details").classList.add("bg-dark", "is-loading")
      fetch(url).then(data => data.json()).then(
        function (response) {
          document.querySelector(".modal-body").innerHTML = response.response
          $('#exampleModalCenter').modal('show')
          e.target.closest(".Details").classList.remove("bg-dark", "is-loading")




        }
      )
    })

  })

  selectProvince = document.getElementById("selectProvince_id")
  selectDistrict = document.getElementById("selectDistrict_id")
  if (selectProvince != null) {
    url = selectProvince.dataset.url

    fetch(url).then(data => data.json()).then(response => {
      selectProvince.disabled = false

      for (let index = 0; index < response.length; index++) {
        let option = document.createElement("option")
        option.innerText = response[index].fields.name
        option.setAttribute("value", response[index].pk)
        selectProvince.appendChild(option)
      }
    })




    selectProvince.addEventListener("change", function (e) {
      selectDistrict.disabled = true

      let id = e.target.options[e.target.options.selectedIndex].attributes[0].value

      let url = selectProvince.dataset.urldis

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(id)
      }).then(data => data.json()).then(response => {
        selectDistrict.innerHTML = ""
        selectDistrict.disabled = false
        let selectfirst = document.createElement("option")
        selectfirst.innerText = "Seleccione ditrito..."
        selectDistrict.appendChild(selectfirst)

        for (let index = 0; index < response.length; index++) {
          let option = document.createElement("option")
          option.innerText = response[index].fields.name
          option.setAttribute("value", response[index].pk)
          selectDistrict.appendChild(option)
        }
      })
    })

  }
  let linkprofile = document.getElementById("profile")
  let lsd = document.getElementById("save-edit-address")
  if (lsd != null) {
    lsd.addEventListener("click", function () {
      let form = document.querySelector("#formAddress_profile")
      let formData = new FormData(form)

      fetch(form.getAttribute("action"), {
        method: "POST",

        body: formData
      }).then(data => data.json()).then(response => console.log(response))
    })
  }
  if (linkprofile != null) {
    linkprofile.addEventListener("click", function () {
      window.location.href = this.dataset.url;
    })
  }

  let adresscomponent = document.getElementsByClassName("address_profile")
  Array.from(adresscomponent).forEach(element => {
    element.addEventListener("click", (e) => {
      Array.from(adresscomponent).forEach(element2 => {
        element2.classList.add("active-adress")


      })
      e.target.classList.remove("active-adress")
      let valdir = e.target.childNodes[2].nextElementSibling.className;

      document.getElementById("method_address").value = "edit"
      document.getElementById("address_profile").value = parseInt(valdir.split("_").pop())
      document.getElementById("description_id").setAttribute("value", e.target.childNodes[7].textContent)
      document.getElementById("description_id").classList.add("active")
      document.getElementById("refrences_id").setAttribute("value", e.target.childNodes[9].textContent.slice(5))
      document.getElementById("refrences_id").classList.add("active")
      document.getElementById("selectProvince_id").value = e.target.childNodes[3].childNodes[0].nextElementSibling.dataset.id
      // document.getElementById("selectProvince_id").setAttribute("value",e.target.childNodes[3].childNodes[0].nextElementSibling.dataset.id)
      // document.getElementById("selectDistrict_id").setAttribute("value",e.target.childNodes[5].childNodes[0].dataset.id)
      let url = selectProvince.dataset.urldis

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(e.target.childNodes[3].childNodes[0].nextElementSibling.dataset.id)
      }).then(data => data.json()).then(response => {
        selectDistrict.innerHTML = ""
        selectDistrict.disabled = false
        let selectfirst = document.createElement("option")
        selectfirst.setAttribute("value", 0)

        selectfirst.innerText = "Seleccione ditrito..."
        selectDistrict.appendChild(selectfirst)

        for (let index = 0; index < response.length; index++) {
          let option = document.createElement("option")
          option.innerText = response[index].fields.name
          option.setAttribute("value", response[index].pk)
          selectDistrict.appendChild(option)
        }
        document.getElementById("selectDistrict_id").value = e.target.childNodes[5].childNodes[0].dataset.id
      
      })

    })
  })
})