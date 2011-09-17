var current = 0

$(document).ready(function() {
	getmore();
}

getmore = function()({
	jQuery.getJSON( '/dash.do', 
		{
			off: current
		},
		function(data) {
			current = current + 40;

			$.each(data, function(i){
				$("<img/>").attr("src", i).appendTo("#content");
		});
});
