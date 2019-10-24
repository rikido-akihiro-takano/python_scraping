;(function($) {




// slide navigation


var initSlideNavigation = function() {
	
	
	var html = "";
	
	
	// add tags
	
	$("body").wrapInner('<div id="overflowContainer"><div id="globalContainer"><div id="bodyContainer"></div></div></div>');
	$("#bgVideoContainer").remove().prependTo("body");
	
	html = '<div id="bodyCover"></div>';
	html += '<div id="slideContainer">';
	html += '<ul id="slideNav"></ul>';
	html += '</div>';
	$("#globalContainer").append(html);
	$(".globalNav li").clone().appendTo("#slideNav");
	
	html = '<li class="hamburger"><div class="hamburgerContainer"><span></span><span></span><span></span></div></li>';
	$(".topNav").append(html);
	
	fixSlideNavigationWidth();
	
	
	// bind events
	
	$(".hamburgerContainer").on("click", function() {
		openSlideNavigation();
	});
	
	$("#bodyCover").on("click", function() {
		closeSlideNavigation();
		return false;
	});
	
	
}


var openSlideNavigation = function() {
	
	
	// slide in
	
	$("#bodyCover").addClass("open");
	$("#globalContainer").css({
		transform: "translateX(-240px)"
		//transform: "translateX(-" + (_windowWidth - 54) + "px)"
	});
	$(".hamburgerContainer").addClass("open");
	
	fixSlideNavigationHeight();
	
	
	// slide out if resized
	
	$(window).on("resize.slideNav", function() {
		if ($(window).width() != _windowWidth) {
			closeSlideNavigation();
		}
	});
	
	
}


var closeSlideNavigation = function(anchor) {
	
	
	// remove resize event
	
	$(window).off("resize.slideNav");
	
	
	// slide out
	
	$("#bodyCover").addClass("close");
	$("#globalContainer").css({
		transform: "translateX(0)"
	});
	$(".hamburgerContainer").removeClass("open");

	setTimeout(function() {
		$("#bodyCover").removeClass();
		$("#overflowContainer, #slideContainer").css({ height: "auto" });
	}, 500);
	
	
}


var fixSlideNavigationWidth = function() {
	
	if (_isSP) {
		
		$("#globalContainer").width(_windowWidth + 240);
		//$("#globalContainer").width(_windowWidth * 2 - 54);
		$("#bodyContainer").width(_windowWidth);
		$("#bodyCover").width(_windowWidth);
		$("#slideContainer").width(240);
		//$("#slideContainer").width(_windowWidth - 54);
		
	} else {
		
		$("#globalContainer").css({ width: "100%" });
		$("#bodyContainer").css({ width: "100%" });
		
	}
	
}


var fixSlideNavigationHeight = function() {
	
	var height = Math.max(
		$("#slideContainer").innerHeight(),
		$(window).height()
	);
	
	$("#overflowContainer, #slideContainer").css({ height: height });
	
}




// pjax


var _pjaxBackButton = true;
var _pjaxBackUrl = "";


var initPjax = function(page) {
	
	
	// init
	
	$("#bodyContainer")
		.wrapInner('<div id="pjaxHead"></div>')
		.append('<div id="pjaxBody"></div>');
	$(".breadcrumbs").after('<section class="lineupHeading hide"></section>');
	$("body").append('<div id="pjaxLoader"><img src="/common/images/2016/loader.gif"></div>');
	
	$.pjax({
		area: "#pjaxBody, .breadcrumbs, .lineupHeading",
		link: "#dummy",
		ajax: {
			timeout: 5000
		},
		wait: 2200,
		fix: {
			reference: false
		},
		load: {
			head: "meta",
			css: false,
			script: false
		}
	});
	
	
	// on click
	
	$(".pjax").one("click", function() {
		
		if (_isSP) {
			location.href = $(this).attr("href");
			return false;
		}
		
		var mousewheelEvent = "onwheel" in document ? "wheel" : "mousewheel";
		$(document).off(mousewheelEvent + ".snap").on(mousewheelEvent + ".pjax", function(e) {
			e.preventDefault();
		});
		
		_pjaxBackButton = false;
		_pjaxBackUrl = location.href;
		
		var loaderTop = (_windowHeight > 600) ? 540 + (_windowHeight - 540) / 2 : _windowHeight / 2;
		
		if (page == "top") {
			
			var idx = $(".topLineup .body a").index($(this));
			
			$(".topLineup .banner").unwrap();
			$("#pjaxHead").addClass("pjaxLoading");
			
			var $banners = $(".topLineup .banner");
			var $bannerTxt = $banners.eq(idx).children(".txt");
			
			var l = (_windowWidth > 979) ? Math.ceil((_windowWidth - 960) / 2) : 40;
			$bannerTxt.css({
				top: $banners.eq(0).height() / 2
			}).animate({
				left: l,
				paddingBottom: 0
			}, 400, "swing", function() {
				$(this).animate({
					top: 342
				}, 800, "easeInOutCubic");
			}).children("img").animate({
				width: 800
			}, 400, "swing");
			
			$banners.each(function(i) {
				if (i == idx) {
					$(this).animate({
						left: 0,
						width: _windowWidth
					}, 400, "swing", function() {
						$("#stage1").css({ visibility: "hidden" });
						var $elms = $("#bgVideoContainer, #stage1, #stage3, #stage4, #stage5, #stage6, #topStageNav, footer");
						$("html, body").animate({ scrollTop: $("#stage2").offset().top }, 800, "easeInOutCubic", function() {
							$elms.remove();
							$(".globalNav li").eq(1).addClass("current");
							$("#pjaxLoader").css({ top: loaderTop }).fadeIn(400);
							$(".header").addClass("show");
						});
					}).animate({
						top: 0,
						height: 540
					}, 800, "easeInOutCubic");
				} else {
					$(this).animate({
						left: 0,
						opacity: 0
					}, 400, "swing");
				}
			});
			
		} else {
			
			var idx = $(".lineupTopList a").index($(this));
			
			$(".lineupTopList .img").unwrap();
			$("#pjaxHead").addClass("pjaxLoading");
			$(".breadcrumbs").addClass("hide");
			
			var $bannersWrapper = $(".lineupTopList ul");
			var $banners = $bannersWrapper.children();
			var $bannerTxt = $banners.eq(idx).children(".txt");
			
			$bannerTxt.css({
				top: 150
			}).animate({
				top: 342,
				paddingBottom: 0
			}, 1200, "easeInOutCubic").children("img").animate({
				width: 800
			}, 1200, "easeInOutCubic");
			
			$bannersWrapper.css({ height: 300 * $banners.length });
			$banners.each(function(i) {
				$(this).css({
					position: "absolute",
					top: 300 * i,
					left: 0,
					width: "100%"
				});
			});
			
			var t = (idx > 4) ? $(".lineupTopLinks").offset().top - _windowHeight : $bannersWrapper.offset().top;
			$("html, body").animate({ scrollTop: t }, 1200, "easeInOutCubic", function() {
				if (idx > 4) $(window).scrollTop($bannersWrapper.offset().top);
				$bannersWrapper.css({ height: _windowHeight });
			});
			
			$banners.each(function(i) {
				if (i == idx) {
					$(this).animate({
						top: (idx > 4) ? 300 * $banners.length - _windowHeight : 0,
						height: 540
					}, 1200, "easeInOutCubic", function() {
						if (idx > 4) $(this).css({ top: 0 });
						$(".pageTitle, .lineupTopLinks, footer").hide().remove();
						$("#pjaxLoader").css({ top: loaderTop }).fadeIn(400);
						$(".header").addClass("show");
					});
				} else {
					$(this).animate({
						opacity: 0
					}, 200, "swing");
				}
			});
			
		}
		
		$.pjax.click($(this).attr("href"));
		
		return false;
		
	});
	
	
	// on fetch
	
	$(document).on('pjax:fetch', pjaxFetch);
	
	
	// on render
	
	$(document).on('pjax:render', function() {
		
		pjaxRender(page);
		
	});
	
	
}


var pjaxFetch = function() {
	
	if (_pjaxBackButton) {
		location.href = _pjaxBackUrl;
	}
	
}


var pjaxRender = function(page) {
	
	_pjaxBackButton = true;
	
	if (page == "top") {
		unsetSnapScroll();
		$(window).off("scroll.stageNav");
	}
	
	smoothScroll();
	fitImages();
	initLightbox();
	initAccordion();
	fixPhoneLinks();
	initLineupSliders();
	
	$("body").css({ backgroundColor: "#fff" });
	$("#pjaxHead").addClass("pjaxLoaded");
	
	if (page == "top") {
		$(".topLineup").remove();
	} else {
		$(".lineupTopList").remove();
	}
	
	setTimeout(function() {
		$("#pjaxLoader").fadeOut(200);
		$("#pjaxBody").fadeIn(1000, function() {
			
			$("body").css({ backgroundColor: "#151825" });
			
			var mousewheelEvent = "onwheel" in document ? "wheel.pjax" : "mousewheel.pjax";
			$(document).off(mousewheelEvent);
			
		});
	}, 100);

	//ga("send", "pageview", window.location.pathname.replace(/^\/?/, "/") + window.location.search);
	
}




// smooth scroll


var smoothScroll = function() {
	
	$("a[href^='#'][href!='#']").on("click", function() {
		
		var href = $(this).attr("href");
		var top = 0;
		
		if ($(href)[0]) {
			top = $(href).offset().top;
		} else {
			if (href != "#top") return false;
		}
		
		$("html, body").animate({ scrollTop: top }, 600, "easeInOutCubic");
		
		return false;
		
	});
	
}




// object-fit image


var fitImages = function() {
	
	$("img.fit").each(function() {
		
		$(this).parent().css({
			backgroundImage: "url(" + $(this).attr("src") + ")",
			backgroundSize: "cover",
			backgroundPosition: "center"
		});
		
	});
	
}




// lightbox


var _lightboxOpen = false;


var initLightbox = function() {
	
	$(".lightbox").on("click", function() {
		
		_lightboxOpen = true;
		
		var scrollPos = $(window).scrollTop();
		var src = $(this).attr("href");
		var isImage = /\.(jpg|png|gif|svg)$/i.test(src);
		var isYoutube = /youtube\.com/i.test(src);
		var loaderTimer;
		
		var content = '<div id="modalContainer"><div id="modalContents">';
		if (isImage) {
			content += '<div id="modalImage"><img src="' + src + '">';
		} else if (isYoutube) {
			content += '<div id="modalYoutube"><div id="modalYoutubeInner"><iframe src="' + src + '?autoplay=1&amp;wmode=transparent" frameborder="0" allowfullscreen></iframe></div>'
		}
		content += '<a href="#" id="modalClose">Close</a></div></div></div>';
		
		$("#overflowContainer").css({ position: "fixed", top: -scrollPos });
		$("body").append('<div id="modalCover"><div id="modalLoader">Loading...</div></div>', content);
		$("#modalCover").fadeIn(300, function() {
			
			loaderTimer = setTimeout(function() {
				$("#modalLoader").fadeIn();
			}, 500);
			
			if (isImage) {
				var img = new Image();
				img.onload = function() {
					clearTimeout(loaderTimer);
					$("#modalLoader").hide();
					$("#modalContainer").fadeIn(200).css({ display: "table" });
				};
				img.src = src;
			} else {
				$("#modalLoader").hide();
				$("#modalContainer").fadeIn(200).css({ display: "table" });
				$(window).scrollTop(0);
			}
			
		});
		
		$("#modalContainer").children().children().on("click", function(e) {
			e.stopPropagation();
		});
		
		$("#modalContainer, #modalCover, #modalClose").one("click", function() {
			
			$("#modalContainer").hide().remove();
			$("#modalCover").fadeOut(600, function() {
				$(this).remove();
			});
			
			setTimeout(function() {
				
				$("#overflowContainer").css({ position: "static", top: 0 });
				$(window).scrollTop(scrollPos);
			
				_lightboxOpen = false;
				
			}, 100);
			
			return false;
			
		});
		
		return false;
		
	});
	
}




// accordion


var initAccordion = function() {
	
	$(".accordionToggle").on("click", function() {
		
		var wrapper = $(this).closest(".accordion").find(".accordionWrapper");
		
		if ($(this).hasClass("open")) {
			wrapper.css({ height: 0 });
			$(this).removeClass("open");
		} else {
			wrapper.css({ height: wrapper.children(".accordionContents").innerHeight() });
			$(this).addClass("open");
		}
		
	});
	
}


var fixAccordionHeight = function() {
	
	$(".accordion").each(function() {
		if ($(this).find(".accordionToggle").hasClass("open")) {
			$(this).find(".accordionWrapper").css({ height: $(this).find(".accordionContents").innerHeight() });
		}
	});
	
}




// section slider


var _sectionSliderNum = 0;
var _sectionSliderIdx = 0;


var initSectionSlider = function() {
	
	var $thumbs = $("#sectionThumbs a");
	var $sections = $("#sectionSlider section");
	_sectionSliderNum = $sections.length;
	
	resizeSectionSlider();
	
	$thumbs.on("click", function() {
		
		var idx = $thumbs.index($(this));
		
		if (idx != _sectionSliderIdx) {
			
			$thumbs.eq(_sectionSliderIdx).removeClass("current");
			$(this).addClass("current");
			
			$sections.eq(idx).css({ height: "auto" });
			
			$("#sectionSlider")
				.css({
					transform: "translateX(-" + _windowWidth * idx + "px)"
				})
				.one("transitionend", function() {
					$sections.eq(_sectionSliderIdx).css({ height: 1 });
					_sectionSliderIdx = idx;
				});
			
		}
		
		return false;
		
	});
	
}


var resizeSectionSlider = function() {
	
	var $sections = $("#sectionSlider section");
	
	$("#sectionSlider").css({
		width: _windowWidth * _sectionSliderNum,
		transform: "translateX(-" + _windowWidth * _sectionSliderIdx + "px)"
	});
	
	$sections.css({ width: _windowWidth });
	
}




// phone link on SP


var _phoneLink = false;


var fixPhoneLinks = function() {
	
	if (_isSP && !_phoneLink) {
		
		$(".phoneLink").each(function() {
			var num = $(this).text();
			$(this).wrap($("<a>").attr("href", "tel:" + num.replace(/-/g, "")));
		});
		
		_phoneLink = true;
		
	} else if (!_isSP && _phoneLink) {
		
		$(".phoneLink").unwrap();
		
		_phoneLink = false;
		
	}
	
}




// top: snap scroll


_snapScroll = false;


var initSnapScroll = function() {
	
	if (_isSP && _snapScroll) {
		unsetSnapScroll();
	} else if (!_isSP && !_snapScroll) {
		setSnapScroll();
	}
	
}


var setSnapScroll = function() {
	
	var stageNum = $(".stageContainer").length;
	var scrolling = false;
	
	var mousewheelEvent = "onwheel" in document ? "wheel.snap" : "mousewheel.snap";
	
	$(document).on(mousewheelEvent, function(e) {
		
		if (scrolling || _lightboxOpen) return;
		
		var currentPos = $(window).scrollTop();
		
		if (currentPos / _windowHeight <= stageNum) {
			var delta = e.originalEvent.deltaY ? -(e.originalEvent.deltaY) : e.originalEvent.wheelDelta;
			if (delta > 0) {
				snap(0, e);
			} else {
				snap(1, e);
			}
		}
		
	}).on("keydown.snap", function(e) {
		
		if (scrolling || _lightboxOpen) return;
		
		var currentPos = $(window).scrollTop();
		
		if (currentPos / _windowHeight <= stageNum) {
			switch (e.which) {
				case 38:
					snap(0, e);
					break;
				case 40:
					snap(1, e);
			}
		}
		
	});
	
	var snap = function(dir, e) {
		
		var currentPos = $(window).scrollTop();
		var i = currentPos / _windowHeight;
		var idx = dir ? Math.ceil(i) : Math.floor(i);
		
		var decimal = parseFloat("0." + (String(i)).split(".")[1]);
		if (decimal < .01 && !dir) idx--;
		if ((decimal > .99 || decimal == 0) && dir) idx++;
		
		var id = "#stage" + (idx + 1);
		if (!$(id)[0]) return;
		
		e.preventDefault();
		scrolling = true;
		
		$("html, body").stop().animate({ scrollTop: $(id).offset().top }, 600, "easeInOutCubic", function() {
			scrolling = false;
		});
		
	}
	
	_bgVideoBottomPos = $("#stage5").offset().top;
	$(window).on("scroll.snap", fixBgVideoPos);
	
	_snapScroll = true;
	
}


var unsetSnapScroll = function() {
	
	var mousewheelEvent = "onwheel" in document ? "wheel.snap" : "mousewheel.snap";
	
	$(document).off(mousewheelEvent + " keydown.snap");
	$(window).off("scroll.snap");
	
	_snapScroll = false;
	
}




// top: background video


_bgVideoList = [];
_bgVideoIdx = 0;
_bgVideoPlaying = false;


var initBgVideo = function() {
	
	$("#bgVideoContainer video").each(function() {
		_bgVideoList.push({
			elem: $(this),
			width: $(this).attr("width"),
			height: $(this).attr("height")
		});
	});
  //テンプレートでシャッフルする為コメントアウト
	//_bgVideoList.shuffle();
	
	fixBgVideoSize();
	playBgVideo(0);
	
}


var fixBgVideoSize = function() {
	
	if (_isSP) {
		if (_bgVideoPlaying) stopBgVideo();
		return;
	} else {
		if (!_bgVideoPlaying) restartBgVideo();
	}
	
	_bgVideoList.forEach(function(value, index) {
		
		if (_windowWidth / _windowHeight > value.width / value.height) {
			value.elem.width(_windowWidth);
			value.elem.height("auto");
		} else {
			value.elem.width("auto");
			value.elem.height(_windowHeight);
		}
		
	});
	
}


var playBgVideo = function(idx) {
	
	_bgVideoList[_bgVideoIdx].elem.hide();
	_bgVideoIdx = idx;
	_bgVideoList[_bgVideoIdx].elem.show();
	
	if (!_isSP) {
		_bgVideoList[_bgVideoIdx].elem[0].muted = true;
		_bgVideoList[_bgVideoIdx].elem[0].play();
		_bgVideoPlaying = true;
	}
	
	_bgVideoList[_bgVideoIdx].elem.one("ended", function() {
		var nextIdx = (_bgVideoIdx == _bgVideoList.length - 1) ? 0 : _bgVideoIdx + 1;
		playBgVideo(nextIdx);
	});
	
}


var stopBgVideo = function() {
	
	_bgVideoList[_bgVideoIdx].elem[0].pause();
	
	_bgVideoPlaying = false;
	
}


var restartBgVideo = function() {
	
	_bgVideoList[_bgVideoIdx].elem[0].play();
	
	_bgVideoPlaying = true;
	
}


_bgVideoFixed = true;
_bgVideoBottomPos = 0;

var fixBgVideoPos = function() {
	
	if ($(window).scrollTop() >= _bgVideoBottomPos) {
		if (_bgVideoFixed) {
			$("#bgVideoContainer").css({ position: "absolute", top: _bgVideoBottomPos });
			_bgVideoFixed = false;
		}
	} else {
		if (!_bgVideoFixed) {
			$("#bgVideoContainer").css({ position: "fixed", top: 0 });
			_bgVideoFixed = true;
		}
	}
	
}




// top: background image


_bgImageList = [];
_bgImageIdx = 0;
_bgImageFading = false;
_bgImageTimer = null;


var initBgImage = function() {
	
	$("#topMainvisualImage li").each(function() {
		_bgImageList.push($(this));
	});
  //テンプレートでシャッフルする為コメントアウト
	//_bgImageList.shuffle();
	
	_bgImageList[0].addClass("show");
	startBgImage();
	
}


var fadeBgImage = function() {
	
	clearTimeout(_bgImageTimer);
	
	_bgImageList[_bgImageIdx].removeClass("show");
	_bgImageIdx = (_bgImageIdx == _bgImageList.length - 1) ? 0 : _bgImageIdx + 1;
	_bgImageList[_bgImageIdx].addClass("show");
	
	_bgImageTimer = setTimeout(fadeBgImage, 5000);
	
}


var startBgImage = function() {
	
	if (_isSP && !_bgImageFading) {
		_bgImageFading = true;
		_bgImageTimer = setTimeout(fadeBgImage, 3000);
	} else if (!_isSP && _bgImageFading) {
		_bgImageFading = false;
		clearTimeout(_bgImageTimer);
	}
	
}




// top: stage navigation


_stageNav = false;


var initStageNav = function() {
	
	
	if (_isSP) {
		if (_stageNav) {
			$(window).off("scroll.stageNav");
			_stageNav = false;
		}
		return;
	} else if (_stageNav) {
		return;
	}
	_stageNav = true;
	
	
	var stageIdx = 1;
	var isVisible = true;
	
	$(window).on("scroll.stageNav", watchScroll);
	watchScroll();
	
	
	function watchScroll() {
		
		if (_lightboxOpen) return;
		
		var t = $(window).scrollTop();
		var idx = Math.floor(t / _windowHeight) + 1;
		var vis = !!(t < _windowHeight * 4.3);
		
		if (!vis && isVisible) {
			isVisible = false;
			$("#topStageNav").stop().fadeOut();
		} else if (vis && !isVisible) {
			isVisible = true;
			$("#topStageNav").stop().fadeIn();
		}
		
		if (idx != stageIdx) {
			$("#topStageNav").children().eq(stageIdx - 1).children().removeClass("current");
			$("#topStageNav").children().eq(idx - 1).children().addClass("current");
		}
		
		stageIdx = idx;
		
	}
	
	
}




// lineup: slider


var _lineupSliderEx, _lineupSliderIn;


var lineupSlider = function(div, duration, easing) {
	
	
	// define
	
	var _this = this;
	
	this.div = $(div);
	this.id = this.div.attr("id");
	
	this.active = !!(this.div.find("li").length > 1);
	if (!this.active) return;
	
	this.idx = 0;
	this.prevIdx = 0;
	this.isSP = _isSP;
	this.animated = false;
	
	this.screenWidth = _windowWidth;
	this.slideWidth = 0;
	
	this.duration = duration || 800;
	this.easing = easing || "swing";
	
	this.slideUl = this.div.children("ul");
	this.slideLi = this.slideUl.children();
	this.len = this.slideLi.length;
	this.slideTxt = $("#" + this.id + "Text").children();
	
	this.touchX = 0;
	this.touchY = 0;
	this.slideX = 0;
	this.touched = false;
	
	
	// add html
	
	var $head = this.slideLi.clone().slice(0, 1);
	var $tail = this.slideLi.clone().slice(-1);
	this.slideUl.prepend($tail);
	this.slideUl.append($head);
	
	
	// button
	
	$("#" + this.id + "Prev").on("click", function() {
		_this.slideBack();
		return false;
	});
	
	$("#" + this.id + "Next").on("click", function() {
		_this.slideNext();
		return false;
	});
	
	
	// swipe
	
	this.slideUl.on("touchstart", function(event) {
		
		if (_this.animated) {
			return;
		}
		
		_this.animated = false;
		_this.touched = true;
		
		_this.touchX = event.originalEvent.changedTouches[0].pageX;
		_this.touchY = event.originalEvent.changedTouches[0].pageY;
		_this.slideX = $(this).position().left;
		
	}).on("touchmove", function(event) {
		
		if (!_this.touched) {
			return;
		}
		
		var x = event.originalEvent.changedTouches[0].pageX;
		var y = event.originalEvent.changedTouches[0].pageY;
		
		if (Math.abs(_this.touchX - x) > Math.abs(_this.touchY - y)) {
			event.preventDefault();
		}
		
		_this.slideX = _this.slideX - (_this.touchX - x);
		$(this).css({ left: _this.slideX });
		
		_this.touchX = x;
		
	}).on("touchend", function(event) {
		
		_this.touched = false;
		
		var w = Math.floor(_this.slideWidth / 2) - 10;
		var x = -(_this.slideWidth * (_this.idx + 1));
		
		if (x - _this.slideX > w) {
			_this.slideNext();
		} else if (_this.slideX - x > w) {
			_this.slideBack();
		} else {
			_this.slide();
		}
		
	});
	
	
}


lineupSlider.prototype = {
	
	
	// slide
	
	slide: function() {
		
		var _this = this;
		
		this.animated = true;
		
		var idx = (this.idx == this.len) ? 0 : (this.idx == -1) ? this.len - 1 : this.idx;
		_this.slideTxt.eq(_this.prevIdx).removeClass("current");
		_this.slideTxt.eq(idx).addClass("current");
		
		this.slideUl.animate({ left: -(this.slideWidth * (this.idx + 1)) }, this.duration, this.easing, function() {
			
			_this.animated = false;
			
			_this.slideX = 0;
			
			if (_this.idx == _this.len) {
				_this.slideUl.css({ left: -_this.slideWidth });
				_this.idx = 0;
			} else if (_this.idx == -1) {
				_this.slideUl.css({ left: -(_this.slideWidth * _this.len) });
				_this.idx = _this.len - 1;
			}
			
			_this.prevIdx = _this.idx;
			
		});
		
	},
	
	slideNext: function() {
		if (!this.animated) {
			this.idx++;
			this.slide();
		}
	},
	
	slideBack: function() {
		if (!this.animated) {
			this.idx--;
			this.slide();
		}
	},
	
	
	// fix size and position
	
	fixSize: function() {
		
		this.slideWidth = (this.isSP) ? this.screenWidth : this.div.width();
		
		this.slideUl.css({
			width: this.slideWidth * (this.len + 2),
			left: -(this.slideWidth * (this.idx + 1))
		});
		
		this.slideUl.children().css({
			width: this.slideWidth
		});
		
	}
	
	
}


var initLineupSliders = function() {
	
	_lineupSliderEx = new lineupSlider("#designExterior", 300, "easeInOutQuad");
	if (_lineupSliderEx.active) setTimeout(function() {
		_lineupSliderEx.fixSize();
	}, 500);
	
	_lineupSliderIn = new lineupSlider("#designInterior", 300, "easeInOutQuad");
	if (_lineupSliderIn.active) setTimeout(function() {
		_lineupSliderIn.fixSize();
	}, 500);
	
}


var resizeLineupSliders = function() {
	
	if (_lineupSliderEx.active) {
		_lineupSliderEx.screenWidth = _windowWidth;
		_lineupSliderEx.isSP = _isSP;
		_lineupSliderEx.fixSize();
	}
	
	if (_lineupSliderIn.active) {
		_lineupSliderIn.screenWidth = _windowWidth;
		_lineupSliderIn.isSP = _isSP;
		_lineupSliderIn.fixSize();
	}
	
}




// array shuffle


Array.prototype.shuffle = function() {
	
	var n = this.length, t, i;
	
	while (n) {
	  i = Math.floor(Math.random() * n--);
	  t = this[n];
	  this[n] = this[i];
	  this[i] = t;
	}
	
	return this;
	
}




// easing


$.extend($.easing, {
	easeOutExpo: function (x, t, b, c, d) {
		return (t == d) ? b + c : c * (-Math.pow(2, -10 * t / d) + 1) + b;
	},
	easeInOutQuad: function (x, t, b, c, d) {
		if ((t /= d / 2) < 1) return c / 2 * t * t + b;
		return -c / 2 * ((--t) * (t - 2) - 1) + b;
	},
	easeInOutCubic: function (x, t, b, c, d) {
		if ((t /= d / 2) < 1) return c / 2 * t * t * t + b;
		return c / 2 * ((t -= 2) * t * t + 2) + b;
	}
});




// on load


var _windowWidth = 0, _windowHeight = 0;
var _isSP = false, _isExistingPage = false;
var _resizeTimer;


$(function() {
	
	
	// init
	
	_windowWidth = $(window).width();
	_windowHeight = $(window).height();
	_isSP = !!($(".globalNav").css("display") == "none");
	_isExistingPage = !!$("#wrapper")[0];
	
	
	if (_isExistingPage) { // existing page
		
		$("body").addClass("existing");
		
		$("header").unwrap();
		initSlideNavigation();
		
		$("#footerPagetop").on("click", function() {
			$("html, body").animate({ scrollTop: 0 }, 600, "easeInOutCubic");
			return false;
		});
		
	} else { // new page
		
		
		// slide navigation
		
		initSlideNavigation();
		
		
		// pjax
		
		if ($(".topMainvisual")[0]) {
			initPjax("top");
		} else if ($(".lineupTopList")[0]) {
			initPjax("lineup");
		}
		
		
		// smooth scroll
		
		smoothScroll();
		
		
		// object-fit image
		
		fitImages();
		
		
		// lightbox
		
		initLightbox();
		
		
		// accordion
		
		initAccordion();
		
		
		// section slider
		
		if ($("#sectionContainer")[0]) {
			initSectionSlider();
		}
		
		
		// phone link on SP
		
		fixPhoneLinks();
		
		
		// top: snap scroll
		
		if ($(".topMainvisual")[0]) {
			initSnapScroll();
		}
		
		
		// top: stage navigation
		
		if ($("#topStageNav")[0]) {
			initStageNav();
		}
		
		
		// top: background video
		
		if ($("#bgVideoContainer")[0]) {
			initBgVideo();
		}
		
		
		// top: background image
		
		if ($("#topMainvisualImage")[0]) {
			initBgImage();
		}
		
		
		// lineup: slider
		
		if ($("#designExterior")[0]) {
			initLineupSliders();
		}
		
		
		// fix anchor position
		
		var hash = location.hash;
		if (hash) {
			$(window).on("load", function() {
				$(this).scrollTop($(hash).offset().top);
			});
		}
		
		
	}
	
	
	// on resize
	
	$(window).on("resize", function() {
		
		if (_resizeTimer !== false) {
			clearTimeout(_resizeTimer);
		}
		
		_resizeTimer = setTimeout(function() {
			
			var w = $(window).width();
			_windowHeight = $(window).height();
			
			if (w != _windowWidth) {
				
				_windowWidth = w;
				_isSP = !!($(".globalNav").css("display") == "none");
				
				fixSlideNavigationWidth();
				
				if (!_isExistingPage) {
					
					fixPhoneLinks();
					
					if ($(".accordion")[0]) {
						fixAccordionHeight();
					}
					
					if ($("#sectionContainer")[0]) {
						resizeSectionSlider();
					}
					
					if ($(".topMainvisual")[0]) {
						initSnapScroll();
						if (!_isSP) {
							_bgVideoBottomPos = $("#stage5").offset().top;
							fixBgVideoPos();
						}
					}
					
					if ($("#topStageNav")[0]) {
						initStageNav();
					}
					
					if ($("#bgVideoContainer")[0]) {
						fixBgVideoSize();
					}
					
					if ($("#topMainvisualImage")[0]) {
						startBgImage();
					}
					
					if ($("#designExterior")[0]) {
						resizeLineupSliders();
					}
					
				}
				
			}
			
		}, 100);
		
	});
	
	
});

})(jQuery);



/*スマホ用　tel*/

$(function() {
    if (!isPhone())
        return;

    $('span[data-action=call]').each(function() {
        var $ele = $(this);
        $ele.wrap('<a href="tel:' + $ele.data('tel') + '"></a>');
    });
});

function isPhone() {
    return (navigator.userAgent.indexOf('iPhone') > 0 || navigator.userAgent.indexOf('Android') > 0);
}

/*オーナー　アコーディオン*/
$(document).ready(function(){
$(".open").click(function(){
$(this).hide();
$(".hide .close").show();
$(this).next().fadeToggle();
});
$(".hide .close").click(function(){
$(this).hide();
$(".open").show();
$(this).parent().hide();
var targetY=$('#section01').offset().top;
$('html,body').animate({scrollTop: targetY},500);
});
});