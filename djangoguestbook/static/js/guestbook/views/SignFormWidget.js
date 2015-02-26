define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/dom-style",
	"dojo/on",
	"dojo/text!./templates/SignFormWidget.html",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetsInTemplateMixin",
	"dijit/form/ValidationTextBox",
	"dijit/form/Button",
	"/static/js/guestbook/models/GreetingStore.js"
], function(declare, baseFx, lang, domStyle, on, template, _WidgetBase,
			_TemplatedMixin, _WidgetsInTemplateMixin, ValidationTextBox, Button, GreetingStore){
	return declare("guestbook.SignFormWidget", [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin ], {
		// Our template - important!
		templateString: template,
		widgetsInTemplate: true,

		// default value
		guestbookName: "default_guestbook",

		postCreate: function(){
			this.inherited(arguments);
			this.own(
				on(this.signButtonNode, "click", lang.hitch(this, "_onclickSignBtn"))
			);
			this.GreetingStore = new GreetingStore();
		},

		_onclickSignBtn : function(){
			this._signNewGreeting(this.GuestbookViewParent,
				this.guestbookNameNode.value,
				this.contentNode.value);
		},

		_signNewGreeting: function(guestbookView, guestbookName, greetingContent){
			var _contentLength = greetingContent.length;
			var _createGreetingDeferred = this.GreetingStore.createGreeting(guestbookName, greetingContent);
				_createGreetingDeferred.then(function(results){
					guestbookView.reloadListGreeting(guestbookName);
				},function(err){
					console.log(err.message);
				}, function(progress){
					console.log(progress);
				})
		},

		_setGuestbookNameAttr: function(guestbookName){
			this.guestbookNameNode.value = guestbookName;
		}
	});
});

