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
let a=0
$(document).ready(function () {
  $(".catCheck").each(function (index2, element2) {
    let arr=  $(this).parent().siblings('ul').find("input[type='checkbox']")
  arr.each(function (index, element) {
      if($(element).attr("checked")){
        console.log("chec");
        $(element2).prop("checked",this.checked)
        $("#cleanCheckFilter").prop("disabled",false)

      }
     
   });
    
  });
  $(".custom-control-input").each(function (index, element) {
    if( $(element).prop("checked"))    $("#cleanFilter").prop("disabled",false)

  });
  $(document).on("click",".Details",function (e) { 
    e.preventDefault();
    const data=fetch("search/"+$(this).attr("tag-url"))
    console.log(data);
  });
});