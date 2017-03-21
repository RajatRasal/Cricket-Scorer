$(document).ready(function(){
	alert('Scoring page');
	//$("[data-toggle='tooltip']").tooltip();
});

$("a.twitter-post").click(function() {
	alert('button clicked');
	// add ajax request here
	$.ajax({
		url: 'http://localhost:9080/',
		dataType: "jsonp",
		jsonpCallback: "callback", // callback parameter
		cache: false,
		timeout: 5000,
		success: function(data) {
			alert(data);
		},
		error: function(jqXHR, textStatus, errorThrown) {
			alert('error ' + textStatus + " " + errorThrown);
		}
	});
});


