var current = 0
var first_post = 0

var first = '<div class="singlePost"><div class="summary">'
var second = '</div> <div class="permalinkLinks"><a href="'
var third = '" class="highresMeta">Hi-res</a> <a href="'
var fourth = '" class="notesMeta">'
var fifth = '</a> </div> <a href="'
var sixth = '" class="hoverMeta" tabindex="1"> <article class="post"> <div class="meta"> <div class="details> <div class="time">'
var seventh = '</div> </div> </div> img src="'
var eigth = '" alt="'
var ninth = '"/> </article> </a> </div>'

getmore = function(){
	jQuery.getJSON( '/dash.do', 
		{
			off: current,
			first: first_post
		},
		function(data) {
			current = current + 40;

			jQuery.each(data, function(i){

				jQuery(concat(first, data[i].caption, second, data[i].hires, third, data[i].perma, '#notes', fourth, data[i].numnotes, fifth, data[i].perma, sixth, data[i].date, seventh, data[i].img, eigth, data[i].caption, ninth)).appendTo("#content");

		});
	});
};

jQuery(document).ready(function() {
	getmore();
});

jQuery(window).scroll(function() {
	if(jQuery(window).scrollTop() + jQuery(window).height() >=
		jQuery(document).height() * .8) {
			getmore();
	}
});

