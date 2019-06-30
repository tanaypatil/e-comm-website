jQuery(function($){

  
  /* ----------------------------------------------------------- */
  /*  2. TOOLTIP
  /* ----------------------------------------------------------- */    
    jQuery('[data-toggle="tooltip"]').tooltip();
    jQuery('[data-toggle2="tooltip"]').tooltip();



    
  /* ----------------------------------------------------------- */
  /*  10. SCROLL TOP BUTTON
  /* ----------------------------------------------------------- */

  //Check to see if the window is top if not then display button

    jQuery(window).scroll(function(){
      if ($(this).scrollTop() > 300) {
        $('.scrollToTop').fadeIn();
      } else {
        $('.scrollToTop').fadeOut();
      }
    });
     
    //Click event to scroll to top

    jQuery('.scrollToTop').click(function(){
      $('html, body').animate({scrollTop : 0},800);
      return false;
    });
  
  /* ----------------------------------------------------------- */
  /*  11. PRELOADER
  /* ----------------------------------------------------------- */

    jQuery(window).load(function() { // makes sure the whole site is loaded      
      jQuery('#wpf-loader-two').delay(200).fadeOut('slow'); // will fade out      
    })

  /* ----------------------------------------------------------- */
  /*  12. GRID AND LIST LAYOUT CHANGER 
  /* ----------------------------------------------------------- */

  jQuery("#list-catg").click(function(e){
    e.preventDefault(e);
    jQuery(".aa-product-catg").addClass("list");
  });
  jQuery("#grid-catg").click(function(e){
    e.preventDefault(e);
    jQuery(".aa-product-catg").removeClass("list");
  });



    
});


function slider() {
    var paginationSlider = ['<i class="fa fa-caret-left"></i>', '<i class="fa fa-caret-right"></i>'];
    var paginationSliderPackages = ['<i class="fa fa-caret-left" style="background-color:#54CCB5;"></i>', '<i class="fa fa-caret-right" style="background-color:#54CCB5;"></i>'];

    if ($('.product-slider').length) {
        $('.product-slider').owlCarousel({
            autoPlay: false,
            slideSpeed: 500,
            navigation: true,
            pagination: false,
            singleItem: true,
            autoHeight: true,
            navigationText: paginationSlider,
            afterAction : syncPosition
        });

        $('.product-slider-thumb').owlCarousel({
            slideSpeed: 500,
            items: 5,
            itemsCustom: [[320, 3],[480, 4], [768, 4], [992, 5], [1200, 5]],
            pagination:false,
            navigation:false,
            navigationText: paginationSlider,
            mouseDrag:false,
            afterInit : function(el){
              el.find(".owl-item").eq(0).addClass("synced");
            }
        });

        $('.review-image-slider').owlCarousel({
            autoPlay: false,
            slideSpeed: 500,
            navigation: true,
            pagination: false,
            singleItem: true,
            autoHeight: true,
            navigationText: paginationSlider
        });

        $('.product-slider-thumb').on("click", ".owl-item", function(e){
            e.preventDefault();
            if($(this).hasClass('synced')){
                return false;
            }else{
                var number = $(this).data("owlItem");
                $('.product-slider').trigger("owl.goTo",number);
            }
        });
    }
}

function syncPosition(el){
    var current = this.currentItem;
    $('.product-slider-thumb')
        .find(".owl-item")
        .removeClass("synced")
        .eq(current)
        .addClass("synced")
    if($('.product-slider-thumb').data("owlCarousel") !== undefined){
        center(current)
    }
}

function center(number){
    var slidethumnailvisible = $('.product-slider-thumb').data("owlCarousel").owl.visibleItems;
    var num = number;
    var found = false;
    for(var i in slidethumnailvisible){
        if(num == slidethumnailvisible[i]) {
            var found = true;
        }
    }

    if(found == false){
        if(num>slidethumnailvisible[slidethumnailvisible.length-1]){
            $('.product-slider-thumb').trigger("owl.goTo", num - slidethumnailvisible.length+2)
        } else {
        if(num - 1 == -1) {
            num = 0;
        }
            $('.product-slider-thumb').trigger("owl.goTo", num);
        }
    } else if(num == slidethumnailvisible[slidethumnailvisible.length-1]) {
        $('.product-slider-thumb').trigger("owl.goTo", slidethumnailvisible[1])
    } else if(num == slidethumnailvisible[0]) {
        $('.product-slider-thumb').trigger("owl.goTo", num-1)
    }
}
$(window).load(function() {
    slider();
});

function upload_img(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img_id').show();
            $('#image_remove').show();
            $('#image_span').show();
            $('#img_id').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}
function upload_img1(input) {
    if (input.files && input.files[0]) {
        var reader1 = new FileReader();

        reader1.onload = function (e) {
            $('#img_id1').show();
            $('#image_remove1').show();
            $('#image_span1').show();
            $('#img_id1').attr('src', e.target.result);
        }

        reader1.readAsDataURL(input.files[0]);
    }
}
function upload_img2(input) {
    if (input.files && input.files[0]) {
        var reader2 = new FileReader();

        reader2.onload = function (e) {
            $('#img_id2').show();
            $('#image_remove2').show();
            $('#image_span2').show();
            $('#img_id2').attr('src', e.target.result);
        }

        reader2.readAsDataURL(input.files[0]);
    }
}

var selector = '.account-section li';

$(selector).on('click', function(){
    $(selector).removeClass('active');
    $(this).addClass('active');
});

$('#ajax_loading_animation').hide();






