(function ($) {
  'use strict';

  // Preloader js    
  $(window).on('load', function () {
    $('.preloader').fadeOut(100);
  });

  // Sticky Menu
  $(window).scroll(function () {
    var height = $('.top-header').innerHeight();
    if ($('header').offset().top > 10) {
      $('.top-header').addClass('hide');
      $('.navigation').addClass('nav-bg');
      $('.navigation').css('margin-top','-'+height+'px');
    } else {
      $('.top-header').removeClass('hide');
      $('.navigation').removeClass('nav-bg');
      $('.navigation').css('margin-top','-'+0+'px');
    }
  });

  // Background-images
  $('[data-background]').each(function () {
    $(this).css({
      'background-image': 'url(' + $(this).data('background') + ')'
    });
  });
  //Bootstrap tooltips
  // $('[data-toggle="tooltip"]').tooltip()

  // venobox popup
  $(document).ready(function () {
    $('.venobox').venobox();
  });

  // Anonymous titles
  // $a := (slice "Elfe" "Lutin" "Ogre" "Narval" "Nain" "Mouton" "Prophète" "Magicien") }}
  //  $title := () }}

})(jQuery);

// Bible Gateway Reference Tagging Tool
BGLinks.version = "BDS";
BGLinks.linkVerses();