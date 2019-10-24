import scrapingCssAndJs

urls=[
 'https://www.oshiire.co.jp/assets/js/vendor/modernizr-2.8.3-respond-1.4.2.min.js',
 'https://www.oshiire.co.jp/assets/js/jquery-1.11.3.min.js',
 'https://www.oshiire.co.jp/shared/js/lib/jquery.belatedPNG.js',
 'https://www.oshiire.co.jp/shared/js/lib/jquery.easing.1.3.js',
 'https://www.oshiire.co.jp/shared/js/lib/jquery.cookie.js',
 'https://www.oshiire.co.jp/shared/js/oshiire.js',
 'https://www.oshiire.co.jp/assets/js/wow.min.js',
 'https://www.oshiire.co.jp/shared/js/lib/mediabox/mootools-core-1.3.2.js',
 'https://www.oshiire.co.jp/shared/js/lib/mediabox/mediaboxAdv.js',
 'https://www.oshiire.co.jp/assets/js/jquery.validationEngine-ja.js',
 'https://www.oshiire.co.jp/assets/js/jquery.validationEngine.js',
 'https://www.oshiire.co.jp/wp-content/plugins/contact-form-7/includes/js/jquery.form.min.js',
 'https://www.oshiire.co.jp/wp-content/plugins/contact-form-7/includes/js/scripts.js',
 'https://www.oshiire.co.jp/wp-includes/js/wp-embed.min.js',
 'https://www.oshiire.co.jp/fc/pio/js/library.js',
 'https://www.oshiire.co.jp/fc/pio/js/jquery.pjax.min.js',
 'https://www.oshiire.co.jp/fc/pio/js/common.js',
 'https://www.oshiire.co.jp/store/js/detail.js',
 'https://www.oshiire.co.jp/shared/js/lib/facebox/facebox.js',
 'https://www.oshiire.co.jp/shared/js/lib/swfobject.js',
 'https://www.oshiire.co.jp/assets/js/anijs-min.js',
 'https://www.oshiire.co.jp/fc/pio/js/common_movie.js',
 'https://www.oshiire.co.jp/fc/pio/js/jquery.flexslider.js',
 'https://www.oshiire.co.jp/fc/pio/js/wow.min.js',
 'https://www.oshiire.co.jp/js/index.js',
 'https://www.oshiire.co.jp/assets/js/device.min.js',
 'https://www.oshiire.co.jp/assets/js/jquery.mb.YTPlayer.js',
 'https://www.oshiire.co.jp/assets/js/custom.js',
 'https://www.oshiire.co.jp/order/js/trunk_form.js',
 'https://www.oshiire.co.jp/assets/js/dcalendar.picker.js',
 'https://www.oshiire.co.jp/lp/js/vendor/slick.min.js',
]

# import元で関数を呼び出す記述があれば、先行してそちらが動いてしまう
scrapingCssAndJs.createDirectoryAndPutFiles(urls)