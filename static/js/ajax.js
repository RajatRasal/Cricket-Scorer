//$('#search-input').keyup(function(e){
//	alert('again');
//});

$('#search-form').submit(function(e){
		alert('again');
		console.log( $(this).serialize() );
		$.post('/ajax_test/', $(this).serialize(), function(data){
			console.log( $('.teams').html(data) );
			$('.teams').html(data);
		}); 
		console.log('here');
		e.preventDefault();
});

//try to add a feature where this works onclick/onchange
//try to add a feature where the function is separate to the method call
$('#team-name-search-form').submit(function(e){
		alert('again');
		console.log( $(this).serialize() );
		$.post('/team_search/', $(this).serialize(), function(data){
			console.log( $('.teams').html(data) );
			$('.teams').html(data);
		}); 
		alert('finished');
		e.preventDefault();
});
