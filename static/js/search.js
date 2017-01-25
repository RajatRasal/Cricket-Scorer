$('#search-form').submit(function(e){
		console.log("form submitted!");
		console.log( $(this).serialize() );
		$.post('/ajax_test/', $(this).serialize(), function(data){
			console.log( $('.teams').html(data) );
			$('.teams').html(data);
		}); 
		console.log('here');
		e.preventDefault();
});
