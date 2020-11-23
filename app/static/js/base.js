$(function() {

  
  new WOW().init();

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
      $(this).parent().next('ul').fadeToggle();
      $(this).toggleClass(function(){
        return $(this).is('.fa-angle-down') ? ($(this).removeClass("fa-angle-down").addClass("fa-angle-up")):($(this).removeClass("fa-angle-up").addClass("fa-angle-down"));
        
      })
      
    });
    $(document).on('change', '.tree input[type=checkbox]', function(e) {
       
      $(this).parent().siblings('ul').find("input[type='checkbox']").prop('checked', this.checked);
      $(this).parentsUntil('.tree').children("input[type='checkbox']").prop('checked', this.checked);
      e.stopPropagation();
    });
   
  });
  