$(document).ready(function(){
	alert('Scoring page');
	scoring(current_data);
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

var current_data = {};

function scoring(x) {
	try {
		alert(x);

		post(x);
	}
	catch(err) {
	}
}

function post(query) {
		$.post('/get_scores/', query, function(data){
			console.log(data);
			current_data = data;
		}); 
}
