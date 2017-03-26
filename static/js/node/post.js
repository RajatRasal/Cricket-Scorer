// Lets require/import the HTTP module
var http = require('http');
var mail = require('nodemailer');

// We need a function which handles requests and send response
function handleRequest(request, response){
	// response.end('It Works!! Path Hit: ' + request.url);
	call_twitter_post();
	response.writeHead(200, {'Content-type':'text/plain'});
	response.end('callback(\'{"message": "Hello"}\')');
}

// Lets define a port we want to listen to
const PORT = 9080; 

// Create a server
var server = http.createServer(handleRequest);

// Lets start our server
server.listen(PORT, function(){
	// Callback triggered when server is successfully listening. Hurray!
	console.log("Server listening on: http://localhost:%s", PORT);
});

// Link with all my Twitter API Keys  
// https://apps.twitter.com/app/13556714/keys
function call_twitter_post() {
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
		var r = Math.floor(Math.random()*100);
		var tweet = {
			status: 'HERE IS A RANDOM NUMBER '.concat(r),
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

// Creates a reusable transporter object taking advantage of SMTP's standards
let transporter = nodemailer.createTransport({
	service: "gmail",
	auth: {
		user: "yugiohrajat1@gmail.com",
	}


