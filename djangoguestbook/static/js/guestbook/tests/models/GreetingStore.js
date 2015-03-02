define([
	"doh/runner",
	"dojo/json",
	"/static/js/sinon/sinon_1_12_1.js",
	"/static/js/guestbook/models/GreetingStore.js"
], function(doh, json, sinon_1_12_1, GreetingStore){

	doh.register("TestGreetingStore", [
		{
			name: "Create_Greeting_Successful",
			setUp: function(){
				greetingStore = new GreetingStore();
				guestbookName = "test_guestbookname";
				greetingContent = "";

				var url = "/api/guestbook/" + guestbookName + "/greeting/";

				this.fakeSuccessData = {
					"data":"Successful data"
				};

				this.fakeserver = sinon.fakeServer.create();
				this.fakeserver.respondWith("POST", url, [
					204,
					{
						"Content-Type": "application/json"
					},
						json.stringify(this.fakeSuccessData)
				])
			},
			runTest: function(){
				var dohDeferred = new doh.Deferred();
				var createGreetingDeferred = greetingStore.createGreeting(guestbookName,
					greetingContent);
				createGreetingDeferred.then(dohDeferred.getTestCallback(function(results){
					var expectation = {
						"data":"Successful data"
					};
					doh.assertEqual(expectation, results);
				}));

				this.fakeserver.respond();
				return dohDeferred;
			},

			tearDown: function(){
				reetingStore = null;
				guestbookName = null;
				greetingContent = null;
				this.fakeserver.restore();
			}
		},
		{
			name: "Create_Greeting_Long_Content",
			setUp: function(){
				greetingStore = new GreetingStore();
				guestbookName = "test_guestbookname";
				greetingContent = "test_greeting_long_content";

				var url = "/api/guestbook/" + guestbookName + "/greeting/";

				this.fakeSuccessData = {
				};

				this.fakeserver = sinon.fakeServer.create();
				this.fakeserver.respondWith("POST", url, [
					404,
					{
						"Content-Type": "application/json"
					},
						json.stringify(this.fakeSuccessData)
				])
			},
			runTest: function(){
				var dohDeferred = new doh.Deferred();
				var createGreetingDeferred = greetingStore.createGreeting(guestbookName,
					greetingContent);
				createGreetingDeferred.then(
					dohDeferred.getTestCallback(function(results){
					console.log("SUCCESS");
					}),
					dohDeferred.getTestCallback(function(error){
					console.log("FAIL");
					var message = error.message;
					doh.assertEqual("This content is empty or length > 10 char", message);
					})
				);

				this.fakeserver.respond();
				return dohDeferred;
			},
			tearDown: function(){
				greetingStore = null;
				guestbookName = null;
				greetingContent = null;
				this.fakeserver.restore();
			}
		},
		{
			name: "GetListGreeting_Successful",
			setUp: function(){
				greetingStore = new GreetingStore();
				guestbookName = "test_guestbookname";

				var url = "/api/guestbook/" + guestbookName + "/greeting/";

				this.fakeSuccessData = {
					"guestbook_name": guestbookName,
					"greetings": [
						{
							"author" : "test_author",
							"content" : "testing",
							"date" : "2015-03-01 09:30 +0000",
							"updated_by" : "update_author",
							"updated_date" : "2015-03-01 10:30 +0000",
							"id_greeting": 1234567890
						}],
					"cursor": "cursor",
					"is_more": false
				}

				this.fakeserver = sinon.fakeServer.create();
				this.fakeserver.respondWith("GET", url, [
					204,
					{
						"Content-Type": "application/json"
					},
					json.stringify(this.fakeSuccessData)
				])
			},
			runTest: function(){
				var thisObject = this;
				var dohDeferred = new doh.Deferred();
				var getListGreetingDeferred = greetingStore.getListGreeting(guestbookName);
				getListGreetingDeferred.then(dohDeferred.getTestCallback(function(results){
					var expectation = {
						"guestbook_name": thisObject.guestbookName,
						"greetings": [
							{
								"author" : "test_author",
								"content" : "testing",
								"date" : "2015-03-01 09:30 +0000",
								"updated_by" : "update_author",
								"updated_date" : "2015-03-01 10:30 +0000",
								"id_greeting": 1234567890
							}],
						"cursor": "cursor",
						"is_more": false
					};
					doh.assertEqual(expectation, results);
				}), dohDeferred.getTestCallback(function(errors){
					console.log("ERROR " + errors.message);
				}));

				this.fakeserver.respond();
				return dohDeferred;
			},
			tearDown: function(){
				greetingStore = null;
				guestbookName = null;
				greetingContent = null;
				this.fakeserver.restore();
			}
		}
	]);
});