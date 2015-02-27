define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/_base/config",
	"dojo/query",
	"dojo/request",
	"dojo/on",
	"dojo/dom",
	"dojo/dom-construct",
	"dijit/registry",
	"./_ViewBaseMixin",
	"./GreetingView",
	"./SignFormWidget",
	"../models/GreetingStore",
	"dojo/text!./templates/GuestbookView.html"
], function(declare, lang, arrayUtil, config, query, request, on, dom, domConstruct,
			registry, _ViewBaseMixin, GreetingView, SignFormWidget,GreetingStore,  template){
	return declare("guestbook.GuestbookView", [_ViewBaseMixin], {
		// Our template - important!
		templateString: template,
		widgetsInTemplate: true,
		autoLoadData: true,

		// Defaut value
		guestbookName: "default_guestbook",

		postCreate: function () {
			this.inherited(arguments);
			this.GreetingStore = new GreetingStore();

			// handle event
			this.own(
				on(this.switchButtonNode, "click", lang.hitch(this, "_onclickSwitchBtn"))
			);
			if (this.autoLoadData){
				// load data
				console.log("before show list greeting")
				this._showListGreeting(this.guestbookName);
			}
			this._showSignGreetingForm();
		},

		_showSignGreetingForm: function(){
			this.signFormWidget = new SignFormWidget({GuestbookViewParent:this});
			this.signFormWidget.placeAt(this.signFormContainerNode);
			this.signFormWidget.startup();
		},

		_showListGreeting: function(guestbookName){
			var guestbookWidgetParent = this;
			var _greetingList = this.GreetingStore.getListGreeting(guestbookName);
			_greetingList.then(function(results){
				var _newDocFrag = document.createDocumentFragment();
				arrayUtil.forEach(results.greetings, function(greeting){
					var greetingView = new GreetingView(greeting);
					// show button delete for admin
					if (config.isAdmin){
						greetingView.setHiddenDeleteNode(false);
						greetingView.setDisabledEditor(false);
					}
					// show button edit if author written
					if (config.userLogin == greeting.author){
						greetingView.setDisabledEditor(false);
					}
					// set guestbook name
					greetingView.setGuestbookName(guestbookName);
					greetingView.setGuestbookParent(guestbookWidgetParent);
					greetingView.placeAt(_newDocFrag);
				});
				domConstruct.place(_newDocFrag, guestbookWidgetParent.greetingsContainerNode);
			}, function(err){
				console.log(err.message);
			}, function(progress){
				console.log(progress);
			});
		},

		_onclickSwitchBtn: function(){
			var guestbookNameLength = this.guestbookNameNode.value;
			this.reloadListGreeting(this.guestbookNameNode.value);
				// set guestbook name for Sign form
			this.signFormWidget._setGuestbookNameAttr(this.guestbookNameNode.value);
		},

		removeGreeting: function(greetingID){
			var widget = registry.byId(greetingID);
			widget.destroy()
		},

		_removeAllGreeting: function(){
			var dom = query(".greetingView");
			for(var i=0; i<dom.length; i++)
			{
				this.removeGreeting(dom[i].id);
			}
		},

		_setGuestbookNameAttr: function(guestbookName){
			this.guestbookNameNode.set("value", guestbookName);
		},

		reloadListGreeting:function(guestbookName){
			this._removeAllGreeting();
			this._showListGreeting(guestbookName);
		}
	});
});