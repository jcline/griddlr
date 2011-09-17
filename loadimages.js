current = 40

$(document).ready(function() {
	getmore();
}

getmore = function()({
	jQuery.getJSON( '/dash.do', 
		{
			offset: current
		},
		function(data) {
			current = current + 40;

			$.each(data, function(i){
				$("<img/>").attr("src", i).appendTo("#content");
		});
});
