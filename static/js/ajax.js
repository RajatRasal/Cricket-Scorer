$(function(){
	console.log('hello');
	$('#team-name-search').keyup(function() {
		console.log('this works');

		$.ajax({
			type: "POST",
			url: "/teamsearch/",
			data: {
				'search_text': $('#team-name-search').val(),
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
			},
			success: searchSuccess,
			dataType: 'html'
		});
	});
});

function search_success(data, textStatus, jqXHR)
{
	$('#search-result').html(data);
}
