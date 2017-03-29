$(document).ready(function(){
	current_data = post();
	console.log('Initial data: ', current_data);
	get_and_set_ball_by_ball_JSON(current_data);
	get_and_set_live_stats(get('live_stats','html'));
	console.log('FINISHED INITIAL');
})

function hide_player_selection_dropdown(){
	// $("#inner-player-selection").hide();
	// document.getElementById("inner-player-selection").css('visibility', 'hidden');
	$("#player-selection").css('visibility', 'hidden'); 
}

function show_player_selection_dropdown(){
	// console.log('show player dropdown');
	// $("#inner-player-selection").show();
	$("#player-selection").css('visibility', 'visible'); 
	// document.getElementById("player-selection").style.visibility = "visible";
	// document.getElementById("inner-player-selection").css('visibility', 'visible');
}

var current_data = {};
var swap = false;

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Live stats displaying functions 
function clear_stats_rows_display(){
	$("tr#batter-1-stats").html('<th scope="row" id="batter-1"></th>');
	$("tr#batter-2-stats").html('<th scope="row" id="batter-2"></th>');
	$("tr#bowler-stats").html('<th scope="row" id="bowler"></th>');
}

function get_and_set_ball_by_ball_JSON(current_data){
	// set_details_for_next_ball();
	$("#over").html(current_data["over"]+'.'+current_data["ball_in_over"]);
	score=current_data["total_runs"]+'/'+current_data["total_wickets"];
	if (current_data["innings"] == 1){
		$("#batting-first").html(score);
	} else {
		$("#batting-second").html(score);
	}

	if (current_data['onstrike'] === null || current_data['onstrike'] === ''){
		console.log('here');
		// Gets all possible options for batter 1 from server 
		// side using the get functions which calls AJAX GET request
		$("div#player-selection").html(get('onstrike', 'html'));
		// Displays the selection box where users can pick which 
		// batter should bat next. 
		show_player_selection_dropdown();
		return false;
	} else {
		// This part of the function will be called once the 
		// choose button is pressed from the onclick event
		// handler of that button. 
		$("#batter-1").html(current_data["onstrike"]);
		// Once the value is set, the dropdown box will close.
		hide_player_selection_dropdown();
	}
	if (current_data["offstrike"] === null || current_data["offstrike"] === "" ){
		$("div#player-selection").html(get('offstrike', 'html'));
		// Displays the selection box where users can pick which 
		// batter should bat next. 
		show_player_selection_dropdown();
		return false;
	} else {
		// This part of the function will be called once the 
		// choose button is pressed from the onclick event
		// handler of that button. 
		$("#batter-2").html(current_data["offstrike"]);
		// Once the value is set, the dropdown box will close.
		hide_player_selection_dropdown();
	}
	if (current_data["bowler"] === null || current_data["bowler"] === "" ){
		$("div#player-selection").html(get('bowler', 'html'));
		// Displays the selection box where users can pick which 
		// batter should bat next. 
		show_player_selection_dropdown()
		return false;
	} else {
		// This part of the function will be called once the 
		// choose button is pressed from the onclick event
		// handler of that button. 
		$("#bowler").html(current_data["bowler"]);
		// Once the value is set, the dropdown box will close.
		hide_player_selection_dropdown();
	}
	return true;
}

function set_player_names_to_current_ball_details(fieldname){
	current_data[fieldname] = $('#names-list').val();
	get_and_set_ball_by_ball_JSON(current_data);
}

function get_and_set_live_stats(live_stats){
	try {
		if (swap === true){
			$("th#batter-2").after(live_stats['onstrike']);
			$("th#batter-1").after(live_stats['offstrike']);
		} else {
			$("th#batter-1").after(live_stats['onstrike']);
			$("th#batter-2").after(live_stats['offstrike']);
		}
		//console.log('batter 1: ',live_stats['onstrike']);
		//console.log('batter 2: ',live_stats['offstrike']);
		//console.log('bowler: ',live_stats['bowler']);
		$("th#bowler").after(live_stats['bowler']);
		//console.log('Last 10 balls: ',live_stats['last_10']);
		$("div#last_10_balls").html(live_stats['last_10']);
	} catch (err) {
		console.log(err);
	}
}

// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Event handler functions for scoring buttons

// Function used to clear any remaining data left over from the previous 
// delivery which is still stored in the returned JSON.
function set_details_for_next_ball(){
	if (swap === true){
		current_data["onstrike"] = [current_data["offstrike"], 
			current_data["offstrike"]=current_data["onstrike"]][0];
	}
	current_data['extras'] = 0;
	current_data['extras_type'] = '';
	current_data['runs'] = 0;
	current_data['how_out'] = '';
}

// Function decides whether batters will have whiched from onstrike
// to offstrike given the number of runs they have scored.
function swap_batters(number){
	// conditional checks for whether number equals 1,3 or 5
	if ( number % 2 === 1 ){
		// swap player names in current_data object
		swap = true;
		//current_data["onstrike"] = [current_data["offstrike"], 
		//	current_data["offstrike"]=current_data["onstrike"]][0];
	 } else {
		 swap = false;
	 }
}

// Below function increments ball count when called. Will be 
// called through the HTML in conjunction with other functions 
// which handle ball by ball events. 
function increment_ball(){
	// increments balls in the over
	current_data['ball_in_over'] += 1;
}

function undo(){
	console.log('undo');
	current_data['people_involved'] = 'UNDO';
	console.log(current_data);
}

function reset_undo(){
	console.log('reset undo');
	console.log(current_data['people_involved']);
	if (current_data['people_involved'] === 'UNDO'){
		console.log('HERE');
		setTimeout(function(){
			console.log('UNDO timeout');},
			1000);
		window.location.reload();
	}
	current_data['people_involved'] = '';
}

// Over will only end when function below is called. 
function end_over(){
	console.log('end over');
	// reset ball in over counter
	current_data['ball_in_over'] = 0;
	// increment over counter 
	current_data['over'] += 1;
	// empty bowler name to select another
	current_data['bowler'] = null;
	// calls get to request server for new bowler name
	// and opens dropdown where new bowler can be selected
	// swap batters 
	swap_batters(1);
	// manually swap batter positions
	set_details_for_next_ball()
	// clear stats rows for to accept new display 
	clear_stats_rows_display()
	// reset the position of the stats 
	// The new bowler stats will not be displayed since
	// the server side db has not yet been updated with
	// new bowler's name 
	get_and_set_live_stats(get('live_stats','html'));
	get_and_set_ball_by_ball_JSON(current_data);
	// window.location.reload(true);
}

function end_innings(){
	// empty batsmen and bowlers
	console.log('end of innings');
	current_data['innings'] = 2;
}

// This function will be called when any of the 0-6 runs buttons 
// on the scoring UI are clicked. It will be called from the 
// 'onclick' event handler and used to set the number of runs 
// scored off a particular ball.
function runs_batting(number){
	console.log('batting runs');
	current_data['runs'] = number;	
	current_data['total_runs'] += number;
	// post(current_data);
	swap_batters(number);
	console.log('Current data: ', current_data);
}

// Prompt box used to confirm the number of extras scored 
// off a delivery if extras have been scored.
function runs_confirmation_box(message){
	// buggy code for testing
	// var extras = parseInt(prompt(message,
	// 	"e.g. 1,2,3,4,5,6").match(/^[123456]$/));
	// console.log(extras); 
	// if (extras === null){	
	//	alert('enter a valid input');
	//	runs_confirmation_box(message);} 
	// return extras;
	var runs = prompt(message,"e.g. 1,2,3,4,5,6")
	console.log('runs confirmation');
	console.log('extras scored: '.concat(runs)); 
	if (runs === null){	
		alert('You must select something\n\
		You can come back and undo it by pressing\
		the undo button');
		return runs_confirmation_box(message);} 
	else {
		if (runs.match(/^[123456]$/) == null){
			alert('enter a valid input');
			return runs_confirmation_box(message);
		} else {
			// converting the input from the prompt 
			// to an integer becuase it is now valid
			return parseInt(runs);
		}
	}
}

// This function will be called when any of the buttons in the  
// 'extras' group in the scoring UI are clicked. It will be 
// called from the 'onclick' event handlers in the html for these 
// buttons. Will be used to set the number of extras scored 
// off a particular ball and the type of extras they were.
function extras_bowling(extras_type, runs){
	// event handler for extras type = 'wides' OR 'noballs'
	current_data['extras_type'] = extras_type;
	current_data['extras'] = runs;
	// Will increment the total runs scored tally.
	current_data['total_runs'] += current_data['extras']; 
	// We want batters to swap on even number of extras  
	swap_batters(current_data['extras']-1);
}

function extras_fielding(extras_type, runs){
	// event handler for extra type = 'byes' OR 'legbyes'
	current_data['extras_type'] = extras_type;
	current_data['extras'] = runs;
	current_data['total_runs'] += current_data['extras']; 
	// We want batters to swap on odd numbers 
	swap_batters(current_data['extras']);
}

function extras_penalties(){
	current_data['extras_type'] = 'penalties';
	current_data['extras'] = 5;
	current_data['total_runs'] += 5; 
	if (confirm("Did batters cross over?") === true){
		swap_batters(1);
	}
}

// buggy short run function
function short_run(runs_taken, runs_short){
	var taken = runs_taken, short = runs_short;
	var scored = taken-short;
	swap_batters(taken);
	current_data['runs'] = scored;
	current_data['total_runs'] += scored;
}

function short_run(){
	var scored = 0;
	while (scored < 1){
		var taken = runs_confirmation_box('How many runs were taken');
		var short = runs_confirmation_box('How many runs were short');
		var scored = taken-short;
		console.log(scored);
		if (scored < 1){alert('Ensure Runs taken < Runs short');}
	}
	swap_batters(taken);
	current_data['runs'] = scored;
	current_data['total_runs'] += scored;
}

function wicket(){
	
	message = "How out?\n1.Bowled\n2.Stumped'\n3.Retired\n\
	4.Run Out\n5.LBW"
	var how_out = prompt(message);
	while (how_out.match(/^[12345]$/) === null){
		how_out = prompt('Try again.',message);
	}
	console.log('how out: ', how_out);

	switch (how_out) {
		case '1': 
			current_data['how_out'] = 'bowled';
			current_data['onstrike'] = null;
			break;
		case '2': 
			current_data['how_out'] = 'stumped';
			current_data['onstrike'] = null;
			break;
		case '3':
			current_data['how_out'] = 'retired';
			current_data[which_batsman()] = null;
			break;
		case '4':
			current_data['how_out'] = 'run out';
			current_data[which_batsman()] = null;
			break;
		case '5':
			current_data['how_out'] = 'LBW';
			current_data['onstrike'] = null;
			break;
	}
	current_data['total_wickets'] += 1;
}

function which_batsman(){
	var which_batsmen = prompt("Which batsman is out?\
		\n1.Onstrike\n2.Offstrike");
	while (which_batsmen.match(/^[12]$/) === null){
		var which_batsmen = prompt("Input error, try again\
			/n1.Onstrike/n2.Offstrike");
	}
	if (which_batsmen == 1){return 'onstrike'}
	else {return 'offstrike'}
}

function end_innings(){
	if (current_data['innings'] === 1){
		// reset all fields which were set during the first
		// innings in preparation for the second
		current_data['total_runs'] = 0;
		current_data['total_wickets'] = 0;
		current_data['innings'] = 2;
		current_data['overs'] = 0;
		current_data['balls_in_over'] = 0;
		current_data['onstrike'] = null;
		current_data['offstrike'] = null;
		current_data['bowler'] = null;
		current_data['how_out'] = '';
		set_details_for_next_ball();
	} else {
		console.log('A team has won');
	}
}

// ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// AJAX Requests or AJAX callers 
$("div#scoring-runs-group button, button#undo").click(function(){
	console.log('EVENT HANDLER');
	// AJAX POST is automatically setting the value for the current
	// data once returned because Javascript is fully pass-by-reference.  
	console.log('data to be sent: ', current_data);
	if (current_data['people_involved'] === 'UNDO'){
		console.log('UNDO EVENT');
		current_data = post(current_data);
		setTimeout(function(){
			window.location.reload();},
			100);
	// if (current_data['
		// PROBLEM WITH POSTING OF THE WICKETS COLUMN
	} else if (current_data['how_out'] != ''){
		console.log('here');
		current_data = post(current_data);
		current_data['how_out'] = '';
		// window.location.reload();},
	} else {
		current_data = post(current_data);
	}
	//current_data = post(current_data);
	console.log('data returned: ', current_data);
	// swapping batsmen in the JSON
	set_details_for_next_ball();
	clear_stats_rows_display();
	// diplaying swapped batsmen
	get_and_set_ball_by_ball_JSON(current_data)
	get_and_set_live_stats(get('live_stats','html'));
	reset_undo();
});

function post(query){
	return $.ajax({
		type: 'POST', // AJAX POST request being made
		// 'contentType' specifies to the server data 
		// that the data that will be sent in the 'data' 
		// header will be in JSON format.
		// BUGGY JSON POST 
		// issue here was that the data being sent was not techniclly in
		// JSON format or being read as JSON by Django, so by specifying 
		// this the code would not work as expected.
		// contentType: "application/json; charset=UTF-8", 
		// URL for data to be sent to.
		url: '/get_scores/', 
		// 'data' header is the actual data being sent 
		// Converts all sending data to JSON format using 
		// stringify.
		// data: JSON.stringify(query), 
		data: query, // { json_string: JSON.stringify(query) }, 
		// 'datatype' header parses all returned data as JSON
		// therefore there is no need to convert response to 
		// JSON using JSON.parse().
		dataType: 'json', 
		success: function(response){
			console.log('POST success');
			console.log(response);
		},
		error: function(jqXHR, textStatus, errorThrown) {
			alert('error ' + textStatus + " " + errorThrown);
		},
		// Turns off asynchronous data transmission so
		// the browser will wait for a reponse before 
		// allowing the code to continue. 
		async: false 
	})['responseJSON'];
}

function get(query, datatype){
	// console.log('QUERY: '.concat(query));
	return $.ajax({
		// default AJAX request type = GET
		// 'contentType' specifies to the server data 
		// that the data that will be sent in the 'data' 
		// header will be in JSON format.
		contentType: "application/json", 
		// URL for data to be sent to.
		url: '/get_scores/', 
		// 'data' header is the actual data being sent 
		// Converts all sending data to JSON format using 
		// stringify.
		data: {'data':query}, 
		// 'datatype' header parses all returned data as JSON
		// therefore there is no need to convert response to 
		// JSON using JSON.parse().
		datatype: datatype, 
		success: function(response){
			console.log('GET successful');
		},
		error: function(jqXHR, textStatus, errorThrown) {
			alert('error ' + textStatus + " " + errorThrown);
		},
		// Turns off asynchronous data transmission so
		// the browser will wait for a reponse before 
		// allowing the code to continue. 
		async: false 
	})['responseJSON'];
}

$("a.twitter-post").click(function(){
	alert('button clicked');
	// add ajax request here
	$.ajax({
		url: 'http://localhost:9080/',
		dataType: "jsonp",
		jsonpCallback: "callback", // callback parameter
		cache: false,
		timeout: 5000,
		success: function(data) {alert(data);},
		error: function(jqXHR, textStatus, errorThrown) {
			alert('error ' + textStatus + " " + errorThrown);
		}
	});
	//var data = {'message':'this'};
	//$.ajax({
	//	url: 'http://localhost:9080/',
	//	type: 'POST',
	//	data: JSON.stringify(data),
	//	contentType: "application/json",
		// complete: callback
	//})
});
