//THIS FILE IS BEING PLACED AT THE END OF THE BODY 
//OF THE INDEX.HTML FILE ALONG WITH THE AJAX.JS FILE.

$(document).ready(function(){
	alert('page loaded');
	$(".next-button").hide();
	alert('another one');
	//$("input#hidden-input").hide();	
	//A 'hacky' was of hiding all the elements 
	//which will be used to send the home and away team names 
	//back to the server side. I was unable to specify these
	//attributes from the server side 'models.py'.
	$("select#id_away_team").hide();	
	$("label[for='id_away_team']").hide();	
	$("select#id_home_team").hide();	
	$("label[for='id_home_team']").hide();	
	//Another 'hacky' was of setting a max and min value for 
	//number of over in the match input field. I was unable to 
	//specify these attributes from the server side 'models.py'.
	$('#id_overs').attr('max', 100).attr('min', 1);
});

//Called by event handlers from various html elements. 
//Will make the next button visible when called. 
//Will be called when the user has provided sufficient information
//in a modal box to allow them to proceed to the next modal box. 
function DisplayNext() {
	$(".next-button").show();
};

//Called by event handlers from various html elements. 
//Will make the next button invisible when called. 
//Will often be called when a new modal box is opened.
function HideNext() {
	$(".next-button").hide();
	$('div#team-name-selection-div').html(' ');
	$('div#player-name-selection-div').html(' ');
};

//This will empty any the team members selected from either team, 
//so that if someone wants to reselect team members, or start a 
//new game after finishing an old one, they can do so when new 
//teams are selected. 
function EmptyTeamArrays() {
	home_team = [];
	away_team = [];
};

$("button.close").click(function() {
	EmptyTeamArrays();
	//alert(home_team);
	DisplayPlayerNames("home-team", []);
	DisplayPlayerNames("away-team", []);
	//remove all search results returned from server side
	//in the html 
	$('.search-results').html(' ');
});

var home_team = [];
var away_team = [];

//Functions is called when a user clicks on a player's name when
//making a team selection. This will check if the player has already
//been selected by consulting either of the above arrays - 'home_team' or 
//'away_team'.
function PlayerNameToggle(sender){
	//alert(sender.id);
	//alert($(sender).attr('value'));
	var player_name = $(sender).attr('value');
	
	//Below IF statements handle the toggling mechanism of the player names.
	//If the player is in the team, then they will be removed
	//from the list by looking up the index of the player name 
	//and remove data at that index using the 'splice' function. 
	//If they are not in the team, they will be 'push'ed onto the 
	//end of their team list. 
	if ( sender.parentNode.className === "home-team" ){
		if ( CheckIfPlayerInTeam(player_name, home_team) ){
			alert('PLAYER IN HOME TEAM');
			var player_name_index = home_team.indexOf(player_name);
			//alert(player_name_index);
			//home_team.splice(player_name_index, player_name_index+1);
			home_team.splice(player_name_index, 1);
		}
		else{
			alert('PLAYER NOT IN HOME TEAM');
			home_team.push(player_name);
		}

		//create a function which displays all the selected player in the sidebar 
		DisplayPlayerNames('home-team', home_team);

		if ( home_team.length === 6 ){
			DisplayNext();
		}

		if ( home_team.length < 6 ){
			HideNext();
		}
	}
	//It is a little repetitive repeating the same sets of code
	//for the home_team and away_team, however with JS being a 
	//pass by value language, this avoid a lot of complications 
	//associated with creating a function to automate this task.
	else{
		alert('away team');
		if ( CheckIfPlayerInTeam(player_name, away_team) ){
			//alert('PLAYER IN AWAY TEAM');
			var player_name_index = away_team.indexOf(player_name);
			away_team.splice(player_name_index, player_name_index+1);
		}
		else{
			//alert('PLAYER NOT IN AWAY TEAM');
			away_team.push(player_name);
		}

		DisplayPlayerNames('away-team', away_team);

		if ( away_team.length === 6 ){
			DisplayNext();
		}

		if ( away_team.length < 6 ){
			HideNext();
		}
	}
	//alert('HOME TEAM');
	//alert(home_team);
	//alert('AWAY TEAM');
	//alert(away_team);	
};

function CheckIfPlayerInTeam(player_name, team_name){
	if (team_name.includes(player_name)) {
		return true
	}
	else{
		return false 
	}
};

function DisplayPlayerNames(team_name, teamsheet){
	//alert('DISPLAY PLAYER NAMES');
	//alert(team_name);
	//alert(teamsheet);
	//Contains the class names given by Bootstrap for special 
	//design features of list elements. These special features will
	//be used to high the captain, vc, wiki and 12th and 13th men.
	var special_display_features = {0:['list-group-item-success','(C)'],
		1:['list-group-item-success','(VC)'],
		2:['list-group-item-warning','(Wk)'],
		11:['list-group-item-danger','12th'],
		12:['list-group-item-danger','13th']};
	var teamsheet_html = '';
	var template = '<li class="list-group-item {class}">{name} \
		<span class="badge"></span> \</li>';
	//alert(teamsheet);
	for (var i = 0; i < teamsheet.length; i++){
		//We insert the name of the player into the list element template
		list_element = template.replace("{name}", teamsheet[i]);
		//If the player is a captain, vc or wiki, they will be
		//either the 1st, 2nd, 3rd clicked. Thus they will be in 
		//0th, 1st or 2nd index of the teamsheet list. If these
		//index numbers are being examined in the for loop, 
		//we shall lookup the specific html class name
		//that should be given to them in the 'special_display_features'
		//list above. This should then be inserted into their 
		//list element template. 
		if ([0,1,2,11,12].indexOf(i) != -1){
			list_element = list_element.replace("{class}", 
				special_display_features[i][0]); 
			//CHROME DOESNT ACCEPT CONCAT AS BEING A VALID FUNCTION 
			//DO FIREFOX AND CHROME TESTS SEPARATELY 
			//TESTING THE STRING.CONCAT SYNTAX
			//list_element = list_element.replace("</span>", 
			//	String.concat(special_display_features[i][1],"</span>")); 
			list_element = list_element.replace("</span>", 
				special_display_features[i][1].concat("</span>")); 
		}
		teamsheet_html += list_element;
	}
	//All the list elements templates created are added to the
	//'teamsheet_html' string. This string is then returned to the
	//web page, and since it contains html markup, the elements 
	//of the list will appear as a html list either under the 
	//home-team or away-team teamsheet, depending on which has 
	//been specified in the 'team_name' argument for this function.
	//var list_tag = 'ul.';
	$('ul.'.concat(team_name)).html(teamsheet_html);
	teamsheet_html = '';	
};


$("form#match-details-submission-form").submit(function(e){
	alert('FINAL SUBMISSION');
	$('<input />').attr('type','hidden'
		).attr('name','home-team'
		).attr('value',home_team
		).appendTo(this);
	$('<input />').attr('type','hidden'
		).attr('name','away-team'
		).attr('value',away_team
		).appendTo(this);
});

