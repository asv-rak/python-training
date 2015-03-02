define([
	"doh/runner",
	"dojo/dom",
	"dojo/json",
	"/static/js/sinon/sinon_1_12_1.js",
	"/static/js/guestbook/views/GuestbookView.js",
	"/static/js/guestbook/models/GreetingStore.js"
], function(doh, dom, json, sinon_1_12_1, GuestbookView, GreetingStore){
	doh.register("TestGuestbookView", [
		{
			name: "Test_Button_Switch_onclick_count",
			runTest: function(){
				var deferred = new doh.Deferred();
				var guestbookView = new GuestbookView();
				var onclickSwitchBtnSpy = sinon.spy(guestbookView, "_onclickSwitchBtn");

				setTimeout(deferred.getTestCallback(function(){
					guestbookView.switchButtonNode.onClick();
					doh.t(onclickSwitchBtnSpy.calledOnce);
					onclickSwitchBtnSpy.restore();
					guestbookView.destroy();
				}), 1000);

				return deferred;
			},
			timeout: 2000
		},
		{
			name: "Test_Load_Greeting_Container",
			setUp: function(){
				this.GreetingStore = new GreetingStore();
				var url = "/api/guestbook/default_guestbook/greeting/";
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
				this.fakeserver.respondWith("GET", url,[
					204,
					{
						"Content-Type": "application/json"
					},
					json.stringify(this.fakeSuccessData)
				])
			},
			runTest: function(){
				var deferred = new doh.Deferred();
				var guestbookView = new GuestbookView();
				var greetingContainer = guestbookView.greetingsContainerNode;
				setTimeout(deferred.getTestCallback(function(){
					doh.is(1, greetingContainer.childElementCount);
					guestbookView.destroy();
				}), 1000);

				this.fakeserver.respond();
				return deferred;
			},
			timeout: 2000
		}
	])
});/**
 * Created by fatatoopc on 3/2/15.
 */
