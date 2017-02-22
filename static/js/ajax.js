//THIS FILE IS BEING PLACED AT THE END OF THE BODY 
//OF THE INDEX.HTML FILE ALONG WITH THE MENUS.JS FILE.

//$('#search-input').keyup(function(e){
//	alert('again');
//});

//Test form 
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

//REAL FORM
//try to add a feature where this works onclick/onchange
//try to add a feature where the function is separate to the method call
//
//AJAX POST
//When the form with the id 'team-name-search-form' is submitted,
//the below function is called.  
$('#team-name-search-form').submit(function(e){
		//alert('team searched');
		//alert($(this).serialize());
	//This is an AJAX routine. It will make a post request to the URL
	//with the path 'team_search', with the team name entered in the form.
	//The server side is listening for a client request at this URL,
	//as seen in the 'urls.py' file in the 'cricket_scoring' dir.
	//'function(data)' parameter speficies a function to run if the 
	//request succeeds. 'Data' holds the data returned from the request.
		$.post('/team_search/', $(this).serialize(), function(data){
			//The data retrieved from the request is now being 
			//passed in between the html tags with the class
			//'teams'.
			$('.teams #team-name-selection-div').html(data);
		}); 
		//alert('finished');
		e.preventDefault();
});

function SubmitTeamName(team_name){
	//alert('team selection');
	//alert(team_name);

	$("input.home-team#team-name-selection-input").val(team_name);
	$("#team-name-selection-form").submit();
	
	//alert('finished');
};


$('#team-name-selection-form').submit(function(e){
		e.preventDefault();
		//alert('team selection submit');
		//akes an AJAX post request to the server side
		$.post('/team_selection/', $(this).serialize(), function(data){
			//console.log( $('.teams #team-name-selection').html(data) );
			//The data retrieved from the server side is now being 
			//passed in between the html tags with the class
			//'home-team' and the id 'player-name-selection-form'
			$('.home-team#player-name-selection-form').html(data);
		});
});
