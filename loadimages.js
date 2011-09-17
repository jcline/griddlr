var current = 0

getmore = function(){
	jQuery.getJSON( '/dash.do', 
		{
			off: current
		},
		function(data) {
			current = current + 40;

			jQuery.each(data, function(i){
				jQuery("<img/>").attr("src", i).appendTo("#content");
		});
	});
});

jQuery(document).ready(function() {
	getmore();
});

