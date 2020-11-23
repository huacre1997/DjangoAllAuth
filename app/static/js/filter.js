$(document).ready(function () {

  window.onload = function () {
    $("#loadingCharge").css("visibility", "hidden");
    $("#loadingSpinner").css("visibility", "hidden");
    imageLoad();
  };
  const imageLoad = () => {
    console.log(document.querySelectorAll(".bk"));
    var x=document.getElementsByClassName("bk");
    var i;
    for (i = 0; i < x.length; i++) {
      x[i].style.visibility = "hidden";
    }
    var container = document.querySelectorAll(".image_container");
    var loadedImageCount = 0,
      imageCount;
    var imgLoad = imagesLoaded(container);
    imgLoad.on("progress", onProgress);
    imgLoad.on("always", onAlways);
    imageCount = imgLoad.images.length;
    console.log(imageCount);
    function onProgress(imgLoad, image) {
      if (image.isLoaded) {
        image.img.parentNode.className = "";

        image.img.parentNode.firstChild.nextSibling.style.visibility = "hidden";
        // image.img.parentNode.nextSibling.nextSibling.style.display="block";
      } else {
        image.img.parentNode.nextSibling.nextSibling.style.display = "none";

        console.log(image.img.parentNode.nextSibling.nextSibling);
        image.img.setAttribute("src", "../static/img/no-imagen.jpg");
        image.img.parentNode.className = "";
        
      }
      loadedImageCount++;
      console.log(loadedImageCount);
      if(loadedImageCount!=imageCount){
        image.img.parentNode.nextSibling.nextSibling.style.visibility="hidden"
        console.log("if");
      }else{
        var i;
        for (i = 0; i < x.length; i++) {
          x[i].style.visibility = "visible";
        }
      }
    }

    function onAlways() {
      console.log("cargo");
    }
  };
  const number = [];
  var url = new URL(window.location.href);
  if (url.searchParams.get("subcategory")) {
    var c = url.searchParams.get("subcategory").split(",");
    c.forEach((element) => {
      number.push(element);
    });
  }
  const renderPage=(dataHtml,url)=>{

    var parser = new DOMParser();
    var doc = parser.parseFromString(dataHtml, "text/html");
    var img = doc.querySelector(".ListProducts");
    document.getElementById("ListProducts").innerHTML = "";
    document.getElementById("ListProducts").appendChild(img);
    window.history.pushState({ page: "another" }, "another page", url);
  }
  const callUrl = async (url) => {
    console.log(url);
    const data = await fetch(url);
    const dataHtml = await data.text();

    renderPage(dataHtml,url)
     

    

    imageLoad();
    $("#loadingCharge").css("visibility", "hidden");
  };

  const removeParam = (key, sourceURL) => {
    var rtn = sourceURL.split("?")[0],
      param,
      params_arr = [],
      queryString =
        sourceURL.indexOf("?") !== -1 ? sourceURL.split("?")[1] : "";
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
  const getIndex = (val) => number.indexOf(val);

  const returnURL = (num) => {
    oldURL = window.location.href;
    if (num.length == 0) {
      $("#cleanCheckFilter").prop("disabled", true);

      console.log("if num=0");
      if (window.location.href.includes("order")) {
        console.log("if includes order");

        // newUrl = removeParam("order", oldURL);

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
  };

  //   FUNCIONES CHECK ||
  $(".subcatCheck").change(function (e) {
    e.preventDefault();
    if ($(this).prop("checked")) {
      number.push($(this).val());
    } else {
      number.splice(getIndex($(this).val()), 1);
    }
    $(".catCheck").each(function (index, element) {
      let a = 0;
      let arreglo = $(element)
        .parent()
        .siblings("ul")
        .find("input[type='checkbox']");
      arreglo.each(function (index, elemente) {
        $(elemente).prop("checked") ? (a += 1) : "";
      });
      a > 0
        ? $(element).prop("checked", true)
        : $(element).prop("checked", false);
    });
    callUrl(returnURL(number));
  });

  $(".catCheck").change(function (e) {
    let arra = $(this).parent().siblings("ul").find("input[type='checkbox']");
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
    oldURL = window.location.href;

    newUrl2 = removeParam("brand", oldURL);

    callUrl(newUrl2.replace(/%2C/g, ","));
    $(".marca").each(function (index, element) {
      $(element).prop("checked", false);
      $("#cleanFilter").prop("disabled", true);
    });
  });
  $("#cleanCheckFilter").click(function (e) {
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
    var x=document.getElementsByClassName("imgProduct");
    var i;
    for (i = 0; i < x.length; i++) {
      x[i].src = "";
    }
    if ($(this).attr("page_number")) {
      oldURL = window.location.href;

      var url = new URL(oldURL);
      url.searchParams.set("page", $(this).attr("page_number")); // setting your param
      var newUrl = url.href;

      callUrl(newUrl.replace(/%2C/g, ","));
    }

    var body = $("html, body");
    body.stop().animate({ scrollTop: 100 }, 500, "swing");
  });
});