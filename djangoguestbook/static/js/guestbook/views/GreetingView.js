define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/dom",
	"dojo/dom-style",
	"dojo/mouse",
	"dojo/on",
	"./_ViewBaseMixin",
	"dijit/InlineEditBox",
	"../models/GreetingStore",
	"dojo/text!./templates/GreetingView.html"
], function(declare, baseFx, lang, dom, domStyle, mouse, on,
			_ViewBaseMixin, InlineEditBox, GreetingStore, template){
	return declare("guestbook.GreetingView", [_ViewBaseMixin], {
		id_greeting: 0,
		author: "Anonymous",
		date: "",
		content: "",
		updated_by: "",
		updated_date: "",

		guestbookName: "default_guestbook",

		// Our template - important!
		templateString: template,

		// A class to be applied to the root node in our template
		baseClass: "greetingView",

		// A reference to our background animation
		mouseAnim: null,

		// Colors for our background animation
		baseBackgroundColor: "#fff",
		mouseBackgroundColor: "#def",
		editBackgroundColor: "#000",

		postCreate: function(){
			// Run any parent postCreate processes - can be done at any point
			this.inherited(arguments);

			// Get a DOM node reference for the root of our widget
			var domNode = this.domNode;

			// Set our DOM node's background color to white -
			// smoothes out the mouseenter/leave event animations
			domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
			// Set up our mouseenter/leave events
			// Using dijit/Destroyable's "own" method ensures that event handlers are unregistered when the widget is destroyed
			// Using dojo/mouse normalizes the non-standard mouseenter/leave events across browsers
			// Passing a third parameter to lang.hitch allows us to specify not only the context,
			// but also the first parameter passed to _changeBackground
			this.own(
				// change background
				on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor, domNode)),
				on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor, domNode)),

				// handle button Delete
				on(this.deleteButtonNode, "click", lang.hitch(this, "_onclickDeleteBtn")),
				// button save in InLineEditText
				on(this.contentNode, "change", lang.hitch(this, "_onclickSaveBtn"))
			);

			this.GreetingStore = new GreetingStore();
		},

		_changeBackground: function(newColor, node) {
			// If we have an animation, stop it
			if (this.mouseAnim) {
				this.mouseAnim.stop();
			}

			// Set up the new animation
			this.mouseAnim = baseFx.animateProperty({
				node: node,
				properties: {
					backgroundColor: newColor
				},
				onEnd: lang.hitch(this, function() {
					// Clean up our mouseAnim property


					this.mouseAnim = null;
				})
			}).play();
		},

		_onclickDeleteBtn: function(){
			var guestbookParent = this.GuestbookViewParent;
			var guestbookName = this.guestbookName;
			var greetingId = this.greetingIdNode.value;
			var deleteGreeting = this.GreetingStore.deleteGreeting(guestbookName, greetingId);
			deleteGreeting.then(function(results){
				guestbookParent.removeGreeting(greetingId);
			}, 	function(err){
				console.log(err.message);
			}, 	function(progress){
				console.log(progress);
			})
		},

		_onclickSaveBtn: function(){
			var guestbookParent = this.GuestbookViewParent;
			var guestbookName = this.guestbookName;
			var greetingContent = this.contentNode.value;
			var greetingId = this.greetingIdNode.value;

			var contentLength = greetingContent.length;
			var _updateGreetingDeferred = this.GreetingStore.updateGreeting(guestbookName, greetingId, greetingContent);
				_updateGreetingDeferred.then(function(results){
					//_guestbookParent.reloadListGreeting(guestbookName);
				},function(err){
					console.log(err.message);
					alert(err.message);
				}, function(progress){
					console.log(progress);
				})
		},

		setHiddenDeleteNode:function(hidden){
			if (hidden){
				domStyle.set(this.deleteButtonNode.domNode, 'visibility', 'hidden');
			} else {
				domStyle.set(this.deleteButtonNode.domNode, 'visibility', 'visible');
			}
		},

		setDisabledEditor: function(disabled){
			this.contentNode._setDisabledAttr(disabled);
		},

		setGuestbookName: function(guestbookName){
			this.guestbookName = guestbookName;
		},

		setGuestbookParent:function(guestbookParent){
			this.GuestbookViewParent = guestbookParent;
		}
	});
});