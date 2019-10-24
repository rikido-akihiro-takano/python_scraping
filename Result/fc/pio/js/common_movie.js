(function($) {

  var $html = $('html');

  // JSによるUI初期化タイミングの遅さをフォローする
  $html.addClass('is-not-ready');

  var mq_device_s = 'screen and (max-width: 899px)';
  var mq_device_l = 'screen and (min-width: 900px)';

  // ドキュメントがモーダルウィンドウ（iframe）として呼ばれる場合
  if (window != window.parent) {
    $('html').addClass('is-in-modal');
  }

  document.addEventListener('DOMContentLoaded', function() {
    // JSによるUI初期化タイミングの遅さフォローおわり
    $html.removeClass('is-not-ready');

    initAreaSearchCollapsible(); // setCollapsible(), setCollapsibleOnlyForSP() よりも前に実行
    setCollapsible();
    setCollapsibleOnlyForSP();
    setGlobalNavigation();
    setStickyHeader();
    setMatchHeight();
    setSmoothScroll();
    showShopAccessMap();
    setPhotoSlider();
    setRoomTypePhotoSlider();
    setInStorePhotoSlider();
    setMovieSlider();
    showPanoramaMovie();
    setModalWindow();
    setPhotoViewer();
  });

  function getUrlParam(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');

    var regex   = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);

    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  function setSmoothScroll() {
    var options = {
          speed : 700,
          easing: 'easeInOutCubic'
        };

    smoothScroll.init(options);
  }

  function setMatchHeight() {
    var targets = [
          '.news-index-2 > li',
          '.review-list-2 > li',
          '.episode-list > li',
          '.promotion-index-2 > li',
          '.index-navigation > li',
          '.index-navigation-2 > li',
          '.service-list > li',
          '.security-flow > li',
          '.media-list > ul > li',
          '.project-info__index > li > a', // IE 11 用（他のブラウザはCSS側で問題なし）
          '.service-guide__heading'
        ];

    $.fn.matchHeight._maintainScroll = true; // Maintain scroll position

    _.each(targets, function(target) {
      $(target).matchHeight();
    });
  }

  function setStickyHeader() {
    var site_header  = document.getElementById('site-header');
    var $site_header = $(site_header);

    if (site_header == null) {
      return false;
    }

    $site_header.addClass('headroom');

    if (window.location.hash) {
      $site_header.addClass('headroom--unpinned');
    } else {
      $site_header.addClass('headroom--pinned');
    }

    var body        = document.getElementsByTagName('body')[0];
    var body_height = site_header.offsetHeight;

    body.style.paddingTop = body_height + 'px';

    var headroom = new Headroom(site_header, {
                     tolerance: {
                       down: 20,
                       up  : 20
                     },
                     offset: body_height * 3
                   });

    headroom.init();
  }

  function setGlobalNavigation() {
    var button       = document.getElementById('global-navigation-button');
    var close_button = document.getElementById('global-navigation-close-button');

    if (button == null) {
      return false;
    }

    var $body   = $('body');
    var nav     = document.getElementById(button.getAttribute('aria-controls'));
    var $nav_bg = $('<div class="global-navigation-bg"></div>').appendTo('body');

    // Init.
    hideNav();

    button.addEventListener('click', function() {
      if (button.getAttribute('aria-expanded') == 'true') {
        hideNav();
      } else {
        showNav();
      }
    });

    close_button.addEventListener('click', function() {
      if (button.getAttribute('aria-expanded') == 'true') {
        hideNav();
      }
    });

    $nav_bg.on('click', function() {
      if (button.getAttribute('aria-expanded') == 'true') {
        hideNav();
      }
    });

    window.addEventListener('resize', function() {
      setPosition();
      setModalBGHeight();
    });

    function showNav() {
      $body.addClass('modal-window-is-opened');
      setPosition();
      setModalBGHeight();

      button.setAttribute('aria-expanded', 'true');

      nav.setAttribute('aria-hidden', 'false');
      nav.setAttribute('tabindex', '0');
      nav.focus();

      $nav_bg.removeClass('is-hidden');
    }

    function hideNav() {
      button.setAttribute('aria-expanded', 'false');

      nav.setAttribute('aria-hidden', 'true');
      nav.setAttribute('tabindex', '-1');

      $body.removeClass('modal-window-is-opened');
      $nav_bg.addClass('is-hidden');
    }

    function setModalBGHeight() {
      $nav_bg.height(document.body.clientHeight + 'px');
    }

    function setPosition() {
      var header_w = document.getElementsByClassName('site-header__inner')[0].clientWidth;

      // この条件においてのみCSSの代わりに位置指定を行う（CSS calc() では表現できない）
      if (header_w < 1000 && window.matchMedia(mq_device_l).matches) {
        nav.style.right = $('.site-header').css('padding-right');
      } else {
        nav.style.right = '';
      }
    }
  }

  function initAreaSearchCollapsible() {
    var tokyo_cities_toggle_button = document.getElementById('tokyo-cities-toggle-button');

    if (tokyo_cities_toggle_button) {
      if (getUrlParam('area') == 'tokyo') {
        tokyo_cities_toggle_button.setAttribute('data-init-opened', 'true');
      }
    }
  }

  function setCollapsible() {
    var buttons = document.getElementsByClassName('js-toggle-collapsible');

    if (buttons.length == 0) {
      return false;
    }

    var boxes = [];

    _.each(buttons, function(button) {
      boxes.push(document.getElementById(button.getAttribute('aria-controls')));
    });

    // Init.

    _.each(buttons, function(button, i) {
      if (button.getAttribute('data-init-opened') == 'true') {
        openCollapsible({button: button, box: boxes[i]});
      } else {
        closeCollapsible({button: button, box: boxes[i]});
      }

      button.addEventListener('click', function(event) {
        event.stopPropagation();
        toggleCollapsible({button: button, box: boxes[i]});
      });
    });

    var button_helpers = document.getElementsByClassName('js-toggle-collapsible-helper');

    _.each(button_helpers, function(helper) {
      helper.addEventListener('click', function() {
        var event = document.createEvent('HTMLEvents');

        event.initEvent('click', false, true);
        helper.getElementsByClassName('js-toggle-collapsible')[0].dispatchEvent(event);
      });
    });

    function toggleCollapsible(param) {
      if (param.button.getAttribute('aria-expanded') == 'false') {
        openCollapsible({button: param.button, box: param.box});
      } else {
        closeCollapsible({button: param.button, box: param.box});
      }
    }

    function openCollapsible(param) {
      var accordion_name = param.button.getAttribute('data-accordion-name');

      // アコーディオン型の場合、グループ化された他のボックスを閉じる
      if (accordion_name) {
        var grouped_buttons = document.querySelectorAll('[data-accordion-name="' + accordion_name + '"]');

        _.each(grouped_buttons, function(button) {
          var box = document.getElementById(button.getAttribute('aria-controls'));

          closeCollapsible({button: button, box: box});
        });
      }

      param.button.setAttribute('aria-expanded', 'true');
      param.box.setAttribute('aria-hidden', 'false');

      var text       = param.button.getAttribute('data-label-opened');
      var path       = param.button.getAttribute('data-path-opened');
      var label      = param.button.querySelector('.js-toggle-collapsible-label');
      var label_elem = label.tagName;

      if (label_elem == 'SPAN') {
        label.textContent = text;
      }

      if (label_elem == 'IMG') {
        label.setAttribute('alt', text);
        label.setAttribute('src', path);
      }
    }

    function closeCollapsible(param) {
      param.button.setAttribute('aria-expanded', 'false');
      param.box.setAttribute('aria-hidden', 'true');

      var text       = param.button.getAttribute('data-label-closed');
      var path       = param.button.getAttribute('data-path-closed');
      var label      = param.button.querySelector('.js-toggle-collapsible-label');
      var label_elem = label.tagName;

      if (label_elem == 'SPAN') {
        label.textContent = text;
      }

      if (label_elem == 'IMG') {
        label.setAttribute('alt', text);
        label.setAttribute('src', path);
      }
    }
  }

  function setCollapsibleOnlyForSP() {
    var buttons = document.getElementsByClassName('js-toggle-collapsible-only-for-sp');

    if (buttons.length == 0) {
      return false;
    }

    var boxes = [];

     _.each(buttons, function(button) {
      boxes.push(document.getElementById(button.getAttribute('aria-controls')));
    });

    var has_eventlistner = false;
    var done_addFeature  = false;

    // Init.

    if (window.matchMedia(mq_device_s).matches) {
      addFeature();
    }

    var button_helpers = document.getElementsByClassName('js-toggle-collapsible-only-for-sp-helper');

    _.each(button_helpers, function(helper) {
      helper.addEventListener('click', function() {
        if (window.matchMedia(mq_device_s).matches) {
          var event = document.createEvent('HTMLEvents');

          event.initEvent('click', false, true);
          helper.getElementsByClassName('js-toggle-collapsible-only-for-sp')[0].dispatchEvent(event);
        }
      });
    });

    window.addEventListener('resize', function() {
      if (window.matchMedia(mq_device_s).matches && done_addFeature == false) {
        addFeature();
      }

      if (window.matchMedia(mq_device_l).matches && done_addFeature == true) {
        removeFeature();
      }
    });

    function addFeature() {
      _.each(buttons, function(button, i) {
        if (button.getAttribute('data-init-opened') == 'true') {
          openCollapsible({button: button, box: boxes[i]});
        } else {
          closeCollapsible({button: button, box: boxes[i]});
        }

        if (has_eventlistner == false) {
          button.addEventListener('click', function(event) {
            event.stopPropagation();
            toggleCollapsible({button: button, box: boxes[i]});
          });
        }
      });

      has_eventlistner = true;
      done_addFeature = true;
    }

    function removeFeature() {
      _.each(buttons, function(button, i) {
        openCollapsible({button: button, box: boxes[i]});
      });

      done_addFeature = false;
    }

    function toggleCollapsible(param) {
      if (param.button.getAttribute('aria-expanded') == 'false') {
        openCollapsible({button: param.button, box: param.box});
      } else {
        closeCollapsible({button: param.button, box: param.box});
      }
    }

    function openCollapsible(param) {
      var accordion_name = param.button.getAttribute('data-accordion-name');

      // アコーディオン型の場合、グループ化された他のボックスを閉じる
      if (accordion_name && window.matchMedia(mq_device_s).matches) {
        var grouped_buttons = document.querySelectorAll('[data-accordion-name="' + accordion_name + '"]');

        _.each(grouped_buttons, function(button) {
          var box = document.getElementById(button.getAttribute('aria-controls'));

          closeCollapsible({button: button, box: box});
        });
      }

      param.button.setAttribute('aria-expanded', 'true');
      param.box.setAttribute('aria-hidden', 'false');

      var text       = param.button.getAttribute('data-label-opened');
      var path       = param.button.getAttribute('data-path-opened');
      var label      = param.button.querySelector('.js-toggle-collapsible-label');
      var label_elem = label.tagName;

      if (label_elem == 'SPAN') {
        label.textContent = text;
      }

      if (label_elem == 'IMG') {
        label.setAttribute('alt', text);
        label.setAttribute('src', path);
      }
    }

    function closeCollapsible(param) {
      param.button.setAttribute('aria-expanded', 'false');
      param.box.setAttribute('aria-hidden', 'true');

      var text       = param.button.getAttribute('data-label-closed');
      var path       = param.button.getAttribute('data-path-closed');
      var label      = param.button.querySelector('.js-toggle-collapsible-label');
      var label_elem = label.tagName;

      if (label_elem == 'SPAN') {
        label.textContent = text;
      }

      if (label_elem == 'IMG') {
        label.setAttribute('alt', text);
        label.setAttribute('src', path);
      }
    }
  }

  function showShopAccessMap() {
    var shop_map = document.querySelector('.shop-map-container');
    var address  = document.querySelector('.shop-page-header__access');

    if (shop_map == null) {
      return false;
    }

    var shop_photo = document.querySelector('.shop-page-header__map-col-1 img.shop-page-header__photo');

    if (shop_photo) {
      shop_photo.addEventListener('load', setMapHeight);
    }
    window.addEventListener('load', setMapHeight);

    google.maps.event.addDomListener(window, 'resize', function() {
      var center = map.getCenter();

      google.maps.event.trigger(map, 'resize');
      map.setCenter(center);
      setMapHeight();
    });

    function setMapHeight() {
      if (shop_photo == null) {
        return false;
      }

      if (window.matchMedia(mq_device_l).matches) {
        shop_map.style.height = (shop_photo.offsetHeight - address.offsetHeight) + 'px';
      } else {
        shop_map.style.height = shop_map.offsetWidth * 0.3 + 'px';
      }
    }

    var lat_lng = new google.maps.LatLng(shop_map.getAttribute('data-lat'), shop_map.getAttribute('data-lng'));

    var map_options = {
          zoom       : 17,
          center     : lat_lng,
          mapTypeId  : google.maps.MapTypeId.ROADMAP,
          scrollwheel: false,
          
        };

    var map = new google.maps.Map(shop_map, map_options);

    new google.maps.Marker({
          position: lat_lng,
          map     : map,
          title   : shop_map.getAttribute('data-title')
        });
  }

  function setPhotoSlider() {
    var slider = document.querySelector('.photo-slider');

    if (slider == null) {
      return false;
    }

    var is_in_modal_on_ios_safari = (window != window.parent) && /iP(ad|hone|od).+Version\/[\d\.]+.*Safari/i.test(navigator.userAgent);
    var is_in_modal_on_ios_chrome = (window != window.parent) && /iP(ad|hone|od).+CriOS\/.*Safari/i.test(navigator.userAgent);

    if (is_in_modal_on_ios_safari || is_in_modal_on_ios_chrome) {
      slider.style.width = slider.offsetWidth + 'px';
    }

    var param = {
          infinite : true,
          speed    : 500,
          autoplay : true,
          dots     : true,
          fade     : true,
          cssEase  : 'linear',
          prevArrow: '<button type="button" class="slick-prev"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M6.513 0l2.121 2.121-4.392 4.392 4.392 4.39-2.121 2.121L0 6.513z"/></svg></button>',
          nextArrow: '<button type="button" class="slick-next"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M2.121 13.024L0 10.903l4.392-4.391L0 2.121 2.121 0l6.513 6.512z"/></svg></button>',
        };

    $(slider).slick(param);
  }

  function setRoomTypePhotoSlider() {
    var param = {
          autoplay    : true,
          slidesToShow: 3,
          centerMode  : true,
          dots        : true,
          prevArrow   : '<button type="button" class="slick-prev"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M6.513 0l2.121 2.121-4.392 4.392 4.392 4.39-2.121 2.121L0 6.513z"/></svg></button>',
          nextArrow   : '<button type="button" class="slick-next"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M2.121 13.024L0 10.903l4.392-4.391L0 2.121 2.121 0l6.513 6.512z"/></svg></button>',
          responsive: [
            {
              breakpoint: 900,
              settings: {
                slidesToShow: 1,
                centerMode  : false
              }
            }
          ]
        };

    $('.room-type-photo-slider').slick(param);
  }

  function setInStorePhotoSlider() {
    var slider = document.querySelector('.in-store-photo-slider');

    if (slider == null) {
      return false;
    }

    var is_in_modal_on_ios_safari = (window != window.parent) && /iP(ad|hone|od).+Version\/[\d\.]+.*Safari/i.test(navigator.userAgent);
    var is_in_modal_on_ios_chrome = (window != window.parent) && /iP(ad|hone|od).+CriOS\/.*Safari/i.test(navigator.userAgent);

    if (is_in_modal_on_ios_safari || is_in_modal_on_ios_chrome) {
      slider.style.width = slider.offsetWidth + 'px';
    }

    var slider_param = {
          infinite : true,
          speed    : 500,
          // autoplay : true,
          fade     : true,
          cssEase  : 'linear',
          prevArrow: '<button type="button" class="slick-prev"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M6.513 0l2.121 2.121-4.392 4.392 4.392 4.39-2.121 2.121L0 6.513z"/></svg></button>',
          nextArrow: '<button type="button" class="slick-next"><svg xmlns="http://www.w3.org/2000/svg" width="8.634" height="13.024" viewBox="0 0 8.634 13.024"><path fill="#FFF" d="M2.121 13.024L0 10.903l4.392-4.391L0 2.121 2.121 0l6.513 6.512z"/></svg></button>',
        };

    var $slider_nav = $('.in-store-photo-slider-navigation');

    $(slider).on('beforeChange', function(event, slick, currentSlide, nextSlide) {
              $slider_nav.find('.slick-slide').removeClass('slick-current').eq(nextSlide).addClass('slick-current');
            })
            .slick(slider_param);

    var nav_param = {
          asNavFor     : '.in-store-photo-slider',
          slidesToShow : $slider_nav.find('.in-store-photo-slider-navigation__item').length,
          dots         : true,
          focusOnSelect: true
        };

    $slider_nav.slick(nav_param);
  }

  function setMovieSlider() {
    var slider = document.querySelector('.movie-slider');

    if (slider == null) {
      return false;
    }

    var is_in_modal_on_ios_safari = (window != window.parent) && /iP(ad|hone|od).+Version\/[\d\.]+.*Safari/i.test(navigator.userAgent);
    var is_in_modal_on_ios_chrome = (window != window.parent) && /iP(ad|hone|od).+CriOS\/.*Safari/i.test(navigator.userAgent);

    if (is_in_modal_on_ios_safari || is_in_modal_on_ios_chrome) {
      slider.style.width = slider.offsetWidth + 'px';
    }

    var slider_param = {
          arrows : false,
          speed  : 500,
          fade   : true,
          cssEase: 'linear'
        };

    var $slider_nav = $('.movie-slider-navigation');
    var videos      = slider.querySelectorAll('video');

    $(slider).on({
                'beforeChange': function(event, slick, currentSlide, nextSlide) {
                  $slider_nav.find('.slick-slide').removeClass('slick-current')
                                                  .eq(nextSlide).addClass('slick-current');
                },
                'afterChange': function() {
                  _.each(videos, function(video) {
                    video.pause();
                    video.currentTime = 0;
                  });

                  var current_video = this.querySelector('.slick-current video');

                  if (current_video) {
                    current_video.play();
                  }
                }
              })
              .slick(slider_param);

    var nav_param = {
          asNavFor     : '.movie-slider',
          slidesToShow : $slider_nav.find('.movie-slider-navigation__item').length,
          dots         : true,
          focusOnSelect: true
        };

    $slider_nav.slick(nav_param);
  }

  function showPanoramaMovie() {
    var target = document.querySelector('.paranoma-movie-container');

    if (target == null) {
      return false;
    }

    embedpano({
      target: target.getAttribute('id'),
      swf   : target.getAttribute('data-swf'),
      xml   : target.getAttribute('data-xml'),
      html5 : 'auto',
      passQueryParameters: true
    });
  }

  function setModalWindow() {
    var open_buttons = document.querySelectorAll('.js-open-modal');

    if (open_buttons.length > 0) {
      var $body         = $('body');
      var wwindowHeight = $(window).height();
      var modalHeight   = Math.floor(wwindowHeight * 0.9);

      var param = {
            className: 'type-doc',
            iframe   : true,
            width    : '90%',
            height   : modalHeight + 'px',
            maxWidth : '1000px',
            close    : '<span>この画面を閉じる</span>',

            onOpen: function() {
              $body.addClass('modal-window-is-opened');
            },

            onClosed: function() {
              $body.removeClass('modal-window-is-opened');
            }
          };

      $(open_buttons).colorbox(param);
    }

    var close_buttons = document.querySelectorAll('.js-close-modal');

    if (close_buttons.length > 0 && window != window.parent) {
      _.each(close_buttons, function(button) {
        button.addEventListener('click', function() {
          parent.$.colorbox.close();
        });
      });
    }
  }

  function setPhotoViewer() {
    var open_buttons = document.querySelectorAll('.js-photo-viewer');

    if (open_buttons.length > 0) {
      var $body = $('body');

      var param = {
            className: 'type-photo',
            close    : '<span>この画面を閉じる</span>',

            onOpen: function() {
              $body.addClass('modal-window-is-opened');
            },

            onClosed: function() {
              $body.removeClass('modal-window-is-opened');
            }
          };

      $(open_buttons).colorbox(param);
    }
  }

}(jQuery));
