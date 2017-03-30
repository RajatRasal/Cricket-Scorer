// require/import the HTTP module
var http = require('http');

// Lets define a port we want to listen to
const PORT = 9080; 

// Create a server
// We need a function which handles requests and send response
var server = http.createServer(function(request, response){
	var message = request.url.replace(/%20/g, " ");
	call_twitter_post(message);
});

// Lets start our server
server.listen(PORT, function(){});

// Link with all my Twitter API Keys  
// https://apps.twitter.com/app/13556714/keys
function call_twitter_post(message){
	// Acts as a import statement to import the 'twit' library specified 
	// as an argument to the require function. This 'twit' library is found 
	// in the 'node_modules' folder inside this directory where the require 
	// function will default to looking inside.
	var Twit = require('twit');
	
	// I have put my Twitter API keys in another file to keep them separate 
	// from this main file. This should make them more secure when rendered 
	// in the page or when put through source control becuase it can will 
	// not add the config file to my open source repositories.
	var config = require('./config');
	
	// T is a twit object, where the twit library handles the interface/socket 
	// connection between my client side JS and the Twitter page whose API 
	// keys I have stored in the config.js file.
	var T = new Twit(config);
	
	// I will create a key-value pair list which will be treated as a JSON 
	// object by the twit object. The keys in the key-value pair list are all 
	// standard keys which are recognised by Twitter in different ways. 
	// e.g the 'status' key stores the data to be posted 
	post_score();
	
	// setInterval(post_score, 1000*20);
	
	function post_score() {
		var tweet = {
			status: message,
		};
		T.post('statuses/update', tweet, after_post);
		
		function after_post(err, data, response){
			if (err) {
				// REMEMEBER that Twitter does not like 
				// the same status being posted twice 
				// so this will more often than not be 
				// the cause of an error!
				console.log("SOMETHING WENT WRONG");
				console.log(err);
			}
			else {
				console.log("IT WORKED!");
			}
		}
	}
}
