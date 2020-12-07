$(function() {

  
  new WOW().init();
    $(".children").find("i").remove()
    $(".children2>.treeview-animated-element>.treeview-animated ").children().unwrap().unwrap().children().unwrap().removeClass("treeview-animated-items").children().removeClass("closed").addClass("treeview-animated-element").next().remove()
    $('#navbar.navbar-right ul li a').click(function() {
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
   
    $(document).on('click', '.tree i', function(e) {
      $(this).parent().siblings('ul').fadeToggle();
      $(this).toggleClass(function(){
        return $(this).is('.fa-angle-right') ? ($(this).removeClass("fa-angle-right").addClass("fa-angle-down")):($(this).removeClass("fa-angle-down").addClass("fa-angle-right"));
        
      })
      
    });
    $(document).on('change', '.tree input[type=checkbox]', function(e) {
       
      $(this).parent().siblings('ul').find("input[type='checkbox']").prop('checked', this.checked);
      $(this).parentsUntil('.tree').children("input[type='checkbox']").prop('checked', this.checked);
      e.stopPropagation();
    });
   
  });
  