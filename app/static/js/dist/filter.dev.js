"use strict";

$(document).ready(function () {
  $("#loadingCharge").css("visibility", "hidden");
  $("#spinnner2").css("visibility", "hidden");
  $(".endless_page_link").each(function (index, element) {
    $(element).removeAttr("href");
  });

  window.onload = function () {};

  var imageLoad = function imageLoad() {
    var container = document.querySelectorAll(".image_container");
    var imgLoad = imagesLoaded(container);
    imgLoad.on("progress", onProgress);
    imgLoad.on("always", onAlways);

    function onProgress(imgLoad, image) {
      var $item = $(image.img).parent();
      $item.removeClass('is-loading');

      if (!image.isLoaded) {
        $item.addClass('is-broken');
      }
    }

    function onAlways() {
      console.log("cargo");
    }
  };

  var number = [];
  var url = new URL(window.location.href);

  if (url.searchParams.get("sc")) {
    var c = url.searchParams.get("sc").split(",");
    c.forEach(function (element) {
      number.push(element);
    });
  }

  imageLoad();

  var callUrl = function callUrl(url) {
    $.ajax({
      type: "POST",
      url: url,
      dataType: "html",
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
        "X-Requested-With": "XMLHttpRequest"
      },
      startTime: performance.now(),
      success: function success(response) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(response, "text/html");
        var firstpagination = doc.querySelectorAll(".pagination")["0"];

        if (firstpagination != undefined) {
          console.log("if");
          doc.querySelectorAll(".pagination")["0"].children[2].classList.add("active");
          var a = 0;
          Array.from(doc.querySelectorAll(".pagination")["0"].children).forEach(function (element) {
            if (element.classList.contains('active')) {
              a += 1;
            }

            ;
          });

          if (a > 1) {
            doc.querySelectorAll(".pagination")["0"].children[2].classList.remove("active");
          } else {
            doc.querySelectorAll(".pagination")["0"].children[2].classList.add("active");
          }
        }

        [].slice.call(doc.querySelectorAll("select.cs-select")).forEach(function (e) {
          new SelectFx(e);
        });
        doc.getElementsByClassName("Details").forEach(function (element) {
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
        var img = doc.querySelector(".ListProducts").children; // var title=doc.querySelector(".titleProducts").textContent
        // var subtitle=doc.querySelector(".subtitle").textContent
        // var results=doc.querySelector(".results").textContent

        $("#ListProducts").text("").append(img);
        window.history.pushState({
          page: "another"
        }, "another page", url);
        var time = performance.now() - this.startTime;
        var seconds = time / 1000;
        seconds = seconds.toFixed(3);
        var result = 'AJAX request took ' + seconds + ' seconds to complete.';
        console.log(result);
        imageLoad();
        $("#loadingCharge").css("visibility", "hidden");
        $("#spinnner2").css("visibility", "hidden");
        var body = $("html, body");
        body.stop().animate({
          scrollTop: 150
        }, 500, "swing");
      }
    });
  }; //   $.ajax({  
  //     type: "post",
  //     url: url,
  //     data:{"method":"next"},
  //     startTime: performance.now(),
  //     success: function (response) {
  //       var parser = new DOMParser();
  //       var doc = parser.parseFromString(response, "text/html");
  //       var img = doc.querySelector(".reviews");
  //       $(".reviews").html(img)
  //        var time = performance.now() - this.startTime;
  //        var seconds = time / 1000;
  //        seconds = seconds.toFixed(3);
  //        var result = 'AJAX request took ' + seconds + ' seconds to complete.';
  //        console.log(result);
  //     }
  // });;


  var removeParam = function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = sourceURL.indexOf("?") !== -1 ? sourceURL.split("?")[1] : "";

    if (queryString !== "") {
      params_arr = queryString.split("&");

      for (var i = params_arr.length - 1; i >= 0; i -= 1) {
        param = params_arr[i].split("=")[0];
        if (param === key) params_arr.splice(i, 1);
      }

      rtn = rtn + "?" + params_arr.join("&");
    }

    return rtn.replace(/%2C/g, ",");
  };

  var getIndex = function getIndex(val) {
    return number.indexOf(val);
  };

  var returnURL = function returnURL(num) {
    oldURL = window.location.href;

    if (num.length == 0) {
      $("#cleanCheckFilter").prop("disabled", true);
      console.log("if num=0");

      if (window.location.href.includes("order")) {
        console.log("if includes order"); // newUrl = removeParam("order", oldURL);

        newUrl = removeParam("page", oldURL);
        newUrl2 = removeParam("sc", oldURL);
        return newUrl2;
      } else {
        console.log("no includes order");
        newUrl = removeParam("sc", oldURL);
        return newUrl;
      }
    } else {
      console.log("number >0");

      if (window.location.href.includes("order")) {
        console.log("number >0 con order");
        var url = new URL(oldURL);
        url.searchParams.set("sc", num.toString()); // setting your param

        var newUrl2 = url.href;
        return newUrl2.replace(/%2C/g, ",");
      }

      var url = new URL(oldURL);
      url.searchParams.set("sc", num.toString()); // setting your param

      var newUrl = url.href;
      newUrl2 = removeParam("page", newUrl);
      return newUrl2.replace(/%2C/g, ",");
    }
  }; //   FUNCIONES CHECK ||


  $(".parentTree >ul.tree>div>.subcatCheck").change(function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    e.preventDefault();
    var arra = $(this).parent().next().find("input");

    if ($(this).prop("checked")) {
      arra.each(function (index, element) {
        if (!number.includes($(this).val())) number.push($(element).val());
      });
    } else {
      arra.each(function (index, element) {
        if (number.includes($(element).val())) {
          number.splice(getIndex($(element).val()), 1);
        }
      });
    }

    console.log(number);
    callUrl(returnURL(number));
  });
  $(".children >ul.tree>div>.subcatCheck").change(function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    e.preventDefault();
    $(this).parent().parent().find("input").each(function (index, element) {
      if ($(element).prop("checked")) {
        number.push($(element).val());
      } else {
        number.splice(getIndex($(element).val()), 1);
      }
    });
    console.log(number);
    $(".parentTree >ul.tree>div>.subcatCheck").each(function (index, element) {
      var a = 0;
      var arreglo = $(this).parent().next().find("input");
      arreglo.each(function (index, elemente) {
        $(elemente).prop("checked") ? a += 1 : "";
      });
      a > 0 ? $(element).prop("checked", true) : $(element).prop("checked", false);
    });
    callUrl(returnURL(number));
  }); // $(".catCheck").change(function (e) {
  //   $("#loadingCharge").css("visibility", "visible");
  //   $("#spinnner2").css("visibility", "visible");
  //   let arra = $(this).parent().siblings("ul").find("input[type='checkbox']");
  //   if ($(this).prop("checked")) {
  //     arra.each(function (index, element) {
  //       if (!number.includes($(this).val())) number.push($(element).val());
  //     });
  //   } else {
  //     arra.each(function (index, element) {
  //       if (number.includes($(element).val())) {
  //         number.splice(getIndex($(element).val()), 1);
  //       }
  //     });
  //   }
  //   callUrl(returnURL(number));
  // });

  $(document).on("change", "#select", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    oldURL = window.location.href;

    if ($(this).val() == "all") {
      console.log("all");
      newUrl2 = removeParam("order", oldURL);
      callUrl(newUrl2.replace(/%2C/g, ","));
    } else {
      var url = new URL(oldURL);
      url.searchParams.set("order", $(this).val()); // setting your param

      var newUrl = url.href;
      callUrl(newUrl.replace(/%2C/g, ","));
    }
  });
  $(".marca").on("change", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    console.log("if");
    oldURL = window.location.href;
    var url = new URL(oldURL);
    url.searchParams.set("brand", $(this).val()); // setting your param

    var newUrl = url.href;
    newUrl2 = removeParam("page", newUrl);
    callUrl(newUrl2.replace(/%2C/g, ","));
  });
  $(".subcatCheck").on("click", function () {
    $("#cleanCheckFilter").prop("disabled", false);
  });
  $(".marca").on("click", function () {
    $("#cleanFilter").prop("disabled", false);
  });
  $(".catCheck").on("click", function () {
    $("#cleanCheckFilter").prop("disabled", false);
  });
  $("#cleanFilter").click(function (e) {
    e.preventDefault();
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    oldURL = window.location.href;
    newUrl2 = removeParam("brand", oldURL);
    callUrl(newUrl2.replace(/%2C/g, ","));
    $(".marca").each(function (index, element) {
      $(element).prop("checked", false);
      $("#cleanFilter").prop("disabled", true);
    });
  });
  $("#cleanCheckFilter").click(function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    number.length = 0;
    e.preventDefault();
    oldURL = window.location.href;
    newUrl2 = removeParam("sc", oldURL);
    callUrl(newUrl2.replace(/%2C/g, ","));
    $(".subcatCheck").each(function (index, element) {
      $(element).prop("checked", false);
      $("#cleanCheckFilter").prop("disabled", true);
    });
  });
  $(document).on("click", ".page-item_list>.page-link", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");

    if (!$(this).is('.active')) {
      $(".page-item").each(function (index, element) {
        $(element).removeClass("active");
      });
    }

    $(this).parent().addClass("active");

    if ($(this).text()) {
      oldURL = window.location.href;
      var url = new URL(oldURL);
      url.searchParams.set("page", $(this).attr("page_number")); // setting your param

      var newUrl = url.href;
      console.log(newUrl);
      callUrl(newUrl.replace(/%2C/g, ","));
    }
  });
  $(document).on("click", ".endless_page_link", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    console.log("ae3a");

    if ($(this).text()) {
      oldURL = window.location.href;
      var url = new URL(oldURL);
      url.searchParams.set("page", $(this).text()); // setting your param

      var newUrl = url.href;
      console.log(newUrl);
      callUrl(newUrl.replace(/%2C/g, ","));
    }
  });
  !function (e) {
    function t(e) {
      return new RegExp("(^|\\s+)" + e + "(\\s+|$)");
    }

    function s(e, t) {
      var s = l(e, t) ? i : n;
      s(e, t);
    }

    var l, n, i;
    "classList" in document.documentElement ? (l = function l(e, t) {
      return e.classList.contains(t);
    }, n = function n(e, t) {
      e.classList.add(t);
    }, i = function i(e, t) {
      e.classList.remove(t);
    }) : (l = function l(e, s) {
      return t(s).test(e.className);
    }, n = function n(e, t) {
      l(e, t) || (e.className = e.className + " " + t);
    }, i = function i(e, s) {
      e.className = e.className.replace(t(s), " ");
    });
    var c = {
      hasClass: l,
      addClass: n,
      removeClass: i,
      toggleClass: s,
      has: l,
      add: n,
      remove: i,
      toggle: s
    };
    "function" == typeof define && define.amd ? define(c) : e.classie = c;
  }(window), function (e) {
    "use strict";

    function t(e, t) {
      if (!e) return !1;

      for (var s = e.target || e.srcElement || e || !1; s && s != t;) {
        s = s.parentNode || !1;
      }

      return s !== !1;
    }

    function s(e, t) {
      for (var s in t) {
        t.hasOwnProperty(s) && (e[s] = t[s]);
      }

      return e;
    }

    function l(e, t) {
      this.el = e, this.options = s({}, this.options), s(this.options, t), this._init();
    }

    l.prototype.options = {
      newTab: !0,
      stickyPlaceholder: !0,
      onChange: function onChange() {
        return !1;
      }
    }, l.prototype._init = function () {
      var e = this.el.querySelector("option[selected]");
      this.hasDefaultPlaceholder = e && e.disabled, this.selectedOpt = e || this.el.querySelector("option"), this._createSelectEl(), this.selOpts = [].slice.call(this.selEl.querySelectorAll("li[data-option]")), this.selOptsCount = this.selOpts.length, this.current = this.selOpts.indexOf(this.selEl.querySelector("li.cs-selected")) || -1, this.selPlaceholder = this.selEl.querySelector("span.cs-placeholder"), this._initEvents();
    }, l.prototype._createSelectEl = function () {
      var e = "",
          t = function t(e) {
        var t = "",
            s = "",
            l = "";
        return !e.selectedOpt || this.foundSelected || this.hasDefaultPlaceholder || (s += "cs-selected ", this.foundSelected = !0), e.getAttribute("data-class") && (s += e.getAttribute("data-class")), e.getAttribute("data-link") && (l = "data-link=" + e.getAttribute("data-link")), "" !== s && (t = 'class="' + s + '" '), "<li " + t + l + ' data-option data-value="' + e.value + '"><span>' + e.textContent + "</span></li>";
      };

      [].slice.call(this.el.children).forEach(function (s) {
        if (!s.disabled) {
          var l = s.tagName.toLowerCase();
          "option" === l ? e += t(s) : "optgroup" === l && (e += '<li class="cs-optgroup"><span>' + s.label + "</span><ul>", [].slice.call(s.children).forEach(function (s) {
            e += t(s);
          }), e += "</ul></li>");
        }
      });
      var s = '<div class="cs-options"><ul>' + e + "</ul></div>";
      this.selEl = document.createElement("div"), this.selEl.className = this.el.className, this.selEl.tabIndex = this.el.tabIndex, this.selEl.innerHTML = '<span class="cs-placeholder">' + this.selectedOpt.textContent + "</span>" + s, this.el.parentNode.appendChild(this.selEl), this.selEl.appendChild(this.el);
    }, l.prototype._initEvents = function () {
      var e = this;
      this.selPlaceholder.addEventListener("click", function () {
        e._toggleSelect();
      }), this.selOpts.forEach(function (t, s) {
        t.addEventListener("click", function () {
          e.current = s, e._changeOption(), e._toggleSelect();
        });
      }), document.addEventListener("click", function (s) {
        var l = s.target;
        e._isOpen() && l !== e.selEl && !t(l, e.selEl) && e._toggleSelect();
      }), this.selEl.addEventListener("keydown", function (t) {
        var s = t.keyCode || t.which;

        switch (s) {
          case 38:
            t.preventDefault(), e._navigateOpts("prev");
            break;

          case 40:
            t.preventDefault(), e._navigateOpts("next");
            break;

          case 32:
            t.preventDefault(), e._isOpen() && "undefined" != typeof e.preSelCurrent && -1 !== e.preSelCurrent && e._changeOption(), e._toggleSelect();
            break;

          case 13:
            t.preventDefault(), e._isOpen() && "undefined" != typeof e.preSelCurrent && -1 !== e.preSelCurrent && (e._changeOption(), e._toggleSelect());
            break;

          case 27:
            t.preventDefault(), e._isOpen() && e._toggleSelect();
        }
      });
    }, l.prototype._navigateOpts = function (e) {
      this._isOpen() || this._toggleSelect();
      var t = "undefined" != typeof this.preSelCurrent && -1 !== this.preSelCurrent ? this.preSelCurrent : this.current;
      ("prev" === e && t > 0 || "next" === e && t < this.selOptsCount - 1) && (this.preSelCurrent = "next" === e ? t + 1 : t - 1, this._removeFocus(), classie.add(this.selOpts[this.preSelCurrent], "cs-focus"));
    }, l.prototype._toggleSelect = function () {
      this._removeFocus(), this._isOpen() ? (-1 !== this.current && (this.selPlaceholder.textContent = this.selOpts[this.current].textContent), classie.remove(this.selEl, "cs-active")) : (this.hasDefaultPlaceholder && this.options.stickyPlaceholder && (this.selPlaceholder.textContent = this.selectedOpt.textContent), classie.add(this.selEl, "cs-active"));
    }, l.prototype._changeOption = function () {
      "undefined" != typeof this.preSelCurrent && -1 !== this.preSelCurrent && (this.current = this.preSelCurrent, this.preSelCurrent = -1);
      var t = this.selOpts[this.current];
      this.selPlaceholder.textContent = t.textContent, this.el.value = t.getAttribute("data-value");
      $("#loadingCharge").css("visibility", "visible");
      $("#spinnner2").css("visibility", "visible");

      if (this.el.value == "all") {
        console.log("all");
        callUrl(removeParam("order", window.location.href).replace(/%2C/g, ","));
      } else {
        var url = new URL(window.location.href);
        url.searchParams.set("order", this.el.value); // setting your param

        var newUrl = url.href;
        callUrl(newUrl.replace(/%2C/g, ","));
      }

      var s = this.selEl.querySelector("li.cs-selected");
      s && classie.remove(s, "cs-selected"), classie.add(t, "cs-selected"), t.getAttribute("data-link") && (this.options.newTab ? e.open(t.getAttribute("data-link"), "_blank") : e.location = t.getAttribute("data-link")), this.options.onChange(this.el.value);
    }, l.prototype._isOpen = function (e) {
      return classie.has(this.selEl, "cs-active");
    }, l.prototype._removeFocus = function () {
      var e = this.selEl.querySelector("li.cs-focus");
      e && classie.remove(e, "cs-focus");
    }, e.SelectFx = l;
  }(window), function () {
    [].slice.call(document.querySelectorAll("select.cs-select")).forEach(function (e) {
      new SelectFx(e);
    });
  }(); // $(document).on("click",".page-item_comment>.page-link", function (e) {
  //   // $("#loadingCharge").css("visibility", "visible");
  //   // $("#spinnner2").css("visibility", "visible");
  //   if(!$(this).is('.active')){
  //   $(".page-item").each(function (index, element) {
  //        $(element).removeClass("active")
  //      });}
  //      $(this).parent().addClass("active")
  //   if ($(this).text()) {
  //     oldURL = window.location.href;
  //     var url = new URL(oldURL);
  //     url.searchParams.set("page", $(this).attr("page_number")); // setting your param
  //     var newUrl = url.href;
  //     callUrlComment(newUrl.replace(/%2C/g, ","));
  //   }
  // });

  var price = [];

  if (url.searchParams.get("price")) {
    var c = url.searchParams.get("price").split(",");
    c.forEach(function (element) {
      price.push(element);
    });
  }

  $(document).on("click", "#priceFilter", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    oldURL = window.location.href;
    e.preventDefault();

    if ($(this).hasClass("active")) {
      price.push(parseInt($("#input-numberMin").val()));
      price.push(parseInt($("#input-numberMax").val()));
      console.log("else");
      var url2 = removeParam("page", oldURL);
      var url3 = new URL(url2);
      url3.searchParams.set("price", price.toString());
      var newUrl = url3.href;
      $(this).text("Quitar filtro");
      callUrl(newUrl.replace(/%2C/g, ","));
    } else {
      console.log("if");
      newUrl2 = removeParam("price", oldURL);
      $(this).text("Aplicar filtro");
      price.length = 0;
      callUrl(newUrl2.replace(/%2C/g, ","));
    }
  });

  var vale = function vale() {
    if (price.length == 0) {
      return [0, 4000];
    } else {
      return price;
    }
  };

  var priceSlider = document.getElementById('slider');

  if (priceSlider) {
    noUiSlider.create(priceSlider, {
      connect: true,
      start: vale(),
      step: 1,
      range: {
        'min': 1,
        'max': 4000
      }
    });
  }

  var inputNumberMin = document.getElementById('input-numberMin');
  var inputNumberMax = document.getElementById('input-numberMax');
  priceSlider.noUiSlider.on('update', function (values, handle) {
    var value = values[handle];

    if (handle) {
      inputNumberMax.value = value;
    } else {
      inputNumberMin.value = value;
    }
  });
  inputNumberMax.addEventListener('change', function () {
    priceSlider.noUiSlider.set([null, this.value]);
  });
  inputNumberMin.addEventListener('change', function () {
    priceSlider.noUiSlider.set([this.value, null]);
  });
  $('.input-number').each(function () {
    var $this = $(this),
        $input = $this.find('input[type="number"]'),
        up = $this.find('.qty-up'),
        down = $this.find('.qty-down');
    down.on('click', function () {
      var value = parseInt($input.val()) - 1;
      value = value < 1 ? 1 : value;
      $input.val(value);
      $input.change();
      updatePriceSlider($this, value);
    });
    up.on('click', function () {
      var value = parseInt($input.val()) + 1;
      $input.val(value);
      $input.change();
      updatePriceSlider($this, value);
    });
  });
  var priceInputMax = document.getElementById('price-max'),
      priceInputMin = document.getElementById('price-min');
  $("#price-max").change(function (e) {
    updatePriceSlider($(this).parent(), this.value);
  });
  $("#price-min").change(function (e) {
    updatePriceSlider($(this).parent(), this.value);
  }); // priceInputMax.addEventListener('change', function(){
  //   updatePriceSlider($(this).parent() , this.value)
  // });
  // priceInputMin.addEventListener('change', function(){
  //   updatePriceSlider($(this).parent() , this.value)
  // });

  function updatePriceSlider(elem, value) {
    if (elem.hasClass('price-min')) {
      console.log('min');
      priceSlider.noUiSlider.set([value, null]);
    } else if (elem.hasClass('price-max')) {
      console.log('max');
      priceSlider.noUiSlider.set([null, value]);
    }
  } //  $(".cat_menu_container").on("click",function (e) { 
  //    console.log("si");
  //    e.preventDefault();
  //    $(this).children("ul").toggle();
  //  });
  // $(document).on("click", ".children >ul.tree", function (e) {
  //   if(!$(this).is('.activate')){
  //   $("#loadingCharge").css("visibility", "visible");
  //   // window.location.href=$(this).attr("tag-url")
  //   $("#spinnner2").css("visibility", "visible");
  //  $(".catFilter").each(function (index, element) {
  //    $(element).parent().parent().removeClass("activate")
  //  });
  //  $(".tree").each(function (index, element) {
  //   $(element).children(":first").removeClass("activate")
  // });
  //     callUrl($(this).children().find(".catFilter").attr("tag-url"));
  //     $(this).toggleClass(function(){
  //       return $(this).is('.activate') ? ($(this).removeClass("activate animated bounceInRight")):($(this).addClass("activate"))
  //     })
  //     console.log($(this).parent().attr("class"));
  //   }
  // });
  // $(document).on("click", ".parentTree >ul.tree>div>.catFilter", function (e) {
  //  if(!$(this).parent().parent().children(":first").is('.activate'))
  //  {
  //    console.log("if");
  //   callUrl($(this).attr("tag-url"));
  //  console.log($(this).attr("tag-url"))
  //   $("#loadingCharge").css("visibility", "visible");
  //   $("#spinnner2").css("visibility", "visible");
  //  $(".tree").each(function (index, element) {
  //    $(element).children(":first").removeClass("activate")
  //  });
  //  $(".catFilter").each(function (index, element) {
  //   $(element).parent().parent().removeClass("activate")
  // });
  //     $(this).toggleClass(function(){
  //       return $(this).parent().parent().children(":first").is('.activate') ? ($(this).parent().parent().children(":first").removeClass("activate animated bounceInRight")):($(this).parent().parent().children(":first").addClass("activate"))
  //     })
  //     console.log($(this).parent().attr("class"));
  //   }
  // });

});