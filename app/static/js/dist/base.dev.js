"use strict";

$(function () {
  new WOW().init();
  $(document).on("click", "#closeModal", function () {
    $(".modal-backdrop").removeClass("modal-backdrop fade show ");
    $("#exampleModal").css("opacity", "0");
  });
  $(document).on("click", "#openModal", function () {
    $("<div class='modal-backdrop  show animate__animated animate__fadeIn'></div>").insertAfter("body");
    $("#exampleModal").css("opacity", "1");
  });

  if (!window.location.href.includes("page")) {
    $(".pagination .page-item_list:nth-child(3)").addClass("active");
  }

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
});