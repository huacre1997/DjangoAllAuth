$(function (e) {


    $(document).mouseup(e => {
        if (!$("#megamenu").is(e.target) && !$("#navbarDropdownMenuLink1").is(e.target)// if the target of the click isn't the container...
        && $("#megamenu").has(e.target).length === 0 ) // ... nor a descendant of the container
        {
            $("#megamenu").removeClass('fadeIn show')


       }
       if (!$("#megamenu2").is(e.target) && !$("#navbarDropdownMenuLink2").is(e.target)// if the target of the click isn't the container...
       && $("#megamenu2").has(e.target).length === 0 ) // ... nor a descendant of the container
       {
           $("#megamenu2").removeClass('fadeIn show')


      }
       if($(".navbar-toggler-icon").is(e.target)){
        $("#megamenu").removeClass('show')

       }
      });
  $(".cat").on("click",async  function (e) {
    e.preventDefault();
    
    console.log($(this));
    $("#spinner").css("display","block");

    clg = $(this).attr("hreft");
    async function spinner(){
    const llegada=await fetch(clg)
     const llegada2=await llegada.json()
     return llegada2
    }
    $("#subcatlist").empty();

    spinner().then(response=>{
        $("#spinner").css("display","none");

        response.forEach((i) => {
          console.log(i);
              $("#subcatlist").append(
                `<li class="sub-title text-uppercase"><a class='nav-item pl-1 mt-2 waves-effect waves-light' href="/subcategory/${i.id}/${i.slug}">${i.name}</a></li>`
              );})
                  
    })
   
            
    //   .then((response) => {
    //     $("#subcatlist").empty();

    //     response.forEach((i) => {
    //       $("#subcatlist").append(
    //         `<li class="sub-title text-uppercase"><a class='nav-item pl-1 mt-2 waves-effect waves-light  '>${i.name}</a></li>`
    //       );
    //     });
    //   });
    $("a.cat.active").removeClass("active");
    $(this).addClass("active");
      
  });
 
  $("#navbarDropdownMenuLink1").on("click",function(e){
    $("#megamenu2").removeClass("show fadeIn")

    $("#megamenu").toggleClass(function(){
        $("a.cat.active").removeClass("active");
        $("#subcatlist").empty();
        return $(this).is('.fadeIn') ? ($(this).removeClass("show fadeIn")):"fadeIn show";
        
      })

  })
 
  $("#navbarDropdownMenuLink2").on("click",function(e){
  
    $("#megamenu").removeClass("show fadeIn")
    $("#megamenu2").toggleClass(function(){

        return $(this).is('.fadeIn') ? ($(this).removeClass("show fadeIn")):"fadeIn show";
        
      })
    
  })

//   $("#navbarDropdownMenuLink1").on("click",function(){
//       $(this).addClass("show")

//       $("#megamenu").toggle(function()
//       {
//           console.log("remove fadeIn");
//               $(this).removeClass("fadeIn").addClass("fadeOut show"); //Adds 'a', removes 'b'

//       }, function() {
//           console.log("remove fadeOut");
//               $(this).removeClass("fadeOut").addClass("fadeIn"); //Adds 'b', removes 'a'

//       });

//   })
  $("#carrImg").hover(
    function () {
      $("#carrIcon").addClass("animated  rubberBand infinite");
    },
    function () {
      $("#carrIcon").removeClass("animated  rubberBand infinite");
    }
  );
  $(document).on("mouseenter",".carrbutton",
    function () {
      $(this).children().toggleClass("animate__animated animate__heartBeat animate__infinite");
    }
  );
  $(document).on("mouseleave",".carrbutton",
    function () {
      $(this).children().removeClass("animate__animated animate__heartBeat animate__infinite");
    }
  );

  $(document).on("mouseenter",".cartEnter",
  function () {
    $("#cartCon").toggleClass("animated  rubberBand infinite");
  }
);
$(document).on("mouseleave",".cartEnter",
  function () {
    $("#cartCon").removeClass("animated  rubberBand  infinite");
  }
);
 
  $("#logout").on("click", function () {
    url = $(this).attr("to");
    location.href = url;
  });
  $("#btnLogin").on("click", function () {
    $("#navbarSupportedContent").removeClass("show");
    url = $(this).attr("hreft");
    console.log(url);
    const login = $.confirm({
      title: "",
      columnClass: "col-lg-5 col-md-7 col-xs-9",
      closeIcon: true,
      content: function () {
        var self = this;
        return $.ajax({
          url: url,
          dataType: "json",
          method: "get",
        })
          .done(function (response) {
            self.setContent(response.html);
          })
          .fail(function () {
            self.setContent("Something went wrong.");
          });
      },
      buttons: {
        okButton: {
          text: "ok",
          action: function () {},
        },
      },
      onContentReady: function () {
        // when content is fetched & rendered in DOM

        this.buttons.okButton.hide();
      },
    });
  });
});
const ajaxfunc = (url) => {};
