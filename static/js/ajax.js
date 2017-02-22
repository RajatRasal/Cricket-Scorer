//THIS FILE IS BEING PLACED AT THE END OF THE BODY 
//OF THE INDEX.HTML FILE ALONG WITH THE MENUS.JS FILE.

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

//AJAX POST
//When the form with the id 'team-name-search-form' is submitted,
//the below function is called.  
$('form#team-name-search-form').submit(function(e){
		alert('team searched');
		//alert($(this).serialize());
		//alert($(this).attr('class'));
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
			$('div#team-name-selection-div').html(data);
			//$('.away-team#team-name-selection-div').html(data);
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


$('form#team-name-selection-form').submit(function(e){
		alert('team name selected'); 
		e.preventDefault();
		//alert('team selection submit');
		//akes an AJAX post request to the server side
		$.post('/team_selection/', $(this).serialize(), function(data){
			//console.log( $('.teams #team-name-selection').html(data) );
			//The data retrieved from the server side is now being 
			//passed in between the html tags with the class
			//'home-team' and the id 'player-name-selection-form'
			$('div#player-name-selection-form').html(data);
		});
});
