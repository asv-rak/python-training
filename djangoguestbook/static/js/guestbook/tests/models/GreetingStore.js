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
				this.GreetingStore = new GreetingStore();
				this.guestbookName = "test_guestbookname";
				this.greetingContent = "";

				var url = "/api/guestbook/" + this.guestbookName + "/greeting/";

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
				var _dohDeferred = new doh.Deferred();
				var _createGreetingDeferred = this.GreetingStore.createGreeting(this.guestbookName,
					this.greetingContent);
				_createGreetingDeferred.then(_dohDeferred.getTestCallback(function(results){
					var expectation = {
						"data":"Successful data"
					};
					doh.assertEqual(expectation, results);
				}));

				this.fakeserver.respond();
				return _dohDeferred;
			},

			tearDown: function(){
				this.GreetingStore = null;
				this.guestbookName = null;
				this.greetingContent = null;
				this.fakeserver.restore();
			}
		},
		{
			name: "Create_Greeting_Long_Content",
			setUp: function(){
				this.GreetingStore = new GreetingStore();
				this.guestbookName = "test_guestbookname";
				this.greetingContent = "test_greeting_long_content";

				var url = "/api/guestbook/" + this.guestbookName + "/greeting/";

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
				var _dohDeferred = new doh.Deferred();
				var _createGreetingDeferred = this.GreetingStore.createGreeting(this.guestbookName,
					this.greetingContent);
				_createGreetingDeferred.then(
					_dohDeferred.getTestCallback(function(results){
					console.log("SUCCESS");
					}),
					_dohDeferred.getTestCallback(function(error){
					console.log("FAIL");
					var message = error.message;
					doh.assertEqual("This content is empty or length > 10 char", message);
					})
				);

				this.fakeserver.respond();
				return _dohDeferred;
			},
			tearDown: function(){
				this.GreetingStore = null;
				this.guestbookName = null;
				this.greetingContent = null;
				this.fakeserver.restore();
			}
		},
		{
			name: "GetListGreeting_Successful",
			setUp: function(){
				this.GreetingStore = new GreetingStore();
				this.guestbookName = "test_guestbookname";

				var url = "/api/guestbook/" + this.guestbookName + "/greeting/";

				this.fakeSuccessData = {
					"guestbook_name": this.guestbookName,
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
				var _thisObject = this;
				var _dohDeferred = new doh.Deferred();
				var _getListGreetingDeferred = this.GreetingStore.getListGreeting(this.guestbookName);
				_getListGreetingDeferred.then(_dohDeferred.getTestCallback(function(results){
					var expectation = {
						"guestbook_name": _thisObject.guestbookName,
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
				}), _dohDeferred.getTestCallback(function(errors){
					console.log("ERROR " + errors.message);
				}));

				this.fakeserver.respond();
				return _dohDeferred;
			},
			tearDown: function(){
				this.GreetingStore = null;
				this.guestbookName = null;
				this.greetingContent = null;
				this.fakeserver.restore();
			}
		}
	]);
});