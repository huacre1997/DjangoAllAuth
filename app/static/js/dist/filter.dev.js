"use strict";

$(document).ready(function () {
  $("#loadingCharge").css("visibility", "hidden");
  $("#spinnner2").css("visibility", "hidden");
  console.log("onload");

  window.onload = function () {};

  var imageLoad = function imageLoad() {
    console.log("imageLoad");
    var x = document.getElementsByClassName("bk");
    var i;

    for (i = 0; i < x.length; i++) {
      x[i].style.visibility = "hidden";
    }

    var container = document.querySelectorAll(".image_container");
    var imgLoad = imagesLoaded(container);
    imgLoad.on("progress", onProgress);
    imgLoad.on("always", onAlways);

    function onProgress(imgLoad, image) {
      console.log(image);

      if (image.isLoaded) {
        console.log("loaded");
        image.img.parentNode.className = "";
        image.img.parentNode.nextSibling.nextSibling.style.visibility = "visible"; // image.img.parentNode.firstChild.nextSibling.style.visibility = "visible";
        // image.img.parentNode.nextSibling.nextSibling.style.display="block";
      } else {
        console.log("no loaded");
        image.img.setAttribute("src", "../static/img/no-imagen.jpg");
        image.img.parentNode.nextSibling.nextSibling.style.display = "none"; // image.img.parentNode.className = "";
      }
    }

    function onAlways() {
      console.log("cargo");
    }
  };

  var number = [];
  var url = new URL(window.location.href);

  if (url.searchParams.get("subcategory")) {
    var c = url.searchParams.get("subcategory").split(",");
    c.forEach(function (element) {
      number.push(element);
    });
  }

  imageLoad();

  var renderPage = function renderPage(dataHtml, url) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(dataHtml, "text/html");
    var img = doc.querySelector(".ListProducts");
    document.getElementById("ListProducts").innerHTML = "";
    document.getElementById("ListProducts").appendChild(img);
    window.history.pushState({
      page: "another"
    }, "another page", url);
  };

  var callUrl = function callUrl(url) {
    // const data = await fetch(url);
    // console.log(data.response);
    // const dataHtml = await data.text();
    // console.log(dataHtml);
    //   console.time('response in');
    $.ajax({
      type: "get",
      url: url,
      startTime: performance.now(),
      success: function success(response) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(response, "text/html");
        var img = doc.querySelector(".ListProducts");
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
          scrollTop: 100
        }, 500, "swing");
      }
    });
    ;
  };

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
        newUrl2 = removeParam("subcategory", oldURL);
        return newUrl2;
      } else {
        console.log("no includes order");
        newUrl = removeParam("subcategory", oldURL);
        return newUrl;
      }
    } else {
      console.log("number >0");

      if (window.location.href.includes("order")) {
        console.log("number >0 con order");
        var url = new URL(oldURL);
        url.searchParams.set("subcategory", num.toString()); // setting your param

        var newUrl = url.href;
        return newUrl2.replace(/%2C/g, ",");
      }

      var url = new URL(oldURL);
      url.searchParams.set("subcategory", num.toString()); // setting your param

      var newUrl = url.href;
      newUrl2 = removeParam("page", newUrl);
      return newUrl2.replace(/%2C/g, ",");
    }
  }; //   FUNCIONES CHECK ||


  $(".subcatCheck").change(function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    e.preventDefault();

    if ($(this).prop("checked")) {
      number.push($(this).val());
    } else {
      number.splice(getIndex($(this).val()), 1);
    }

    $(".catCheck").each(function (index, element) {
      var a = 0;
      var arreglo = $(element).parent().siblings("ul").find("input[type='checkbox']");
      arreglo.each(function (index, elemente) {
        $(elemente).prop("checked") ? a += 1 : "";
      });
      a > 0 ? $(element).prop("checked", true) : $(element).prop("checked", false);
    });
    callUrl(returnURL(number));
  });
  $(".catCheck").change(function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    var arra = $(this).parent().siblings("ul").find("input[type='checkbox']");

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

    callUrl(returnURL(number));
  });
  $("#select").on("change", function (e) {
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
    e.preventDefault();
    oldURL = window.location.href;
    newUrl2 = removeParam("subcategory", oldURL);
    callUrl(newUrl2.replace(/%2C/g, ","));
    $(".custom-control-input").each(function (index, element) {
      $(element).prop("checked", false);
      $("#cleanCheckFilter").prop("disabled", true);
    });
  });
  $(document).on("click", ".page-link", function (e) {
    $("#loadingCharge").css("visibility", "visible");
    $("#spinnner2").css("visibility", "visible");
    var x = document.getElementsByClassName("imgProduct");
    var i;

    for (i = 0; i < x.length; i++) {
      x[i].src = "";
      x[i].parentNode.className = "image_container";
      x[i].parentNode.nextSibling.nextSibling.style.display = "block";
      x[i].parentNode.firstChild.nextSibling.style.visibility = "visible";
    }

    if ($(this).attr("page_number")) {
      oldURL = window.location.href;
      console.log(oldURL);
      var url = new URL(oldURL);
      url.searchParams.set("page", $(this).attr("page_number")); // setting your param

      var newUrl = url.href;
      callUrl(newUrl.replace(/%2C/g, ","));
    }
  });
});