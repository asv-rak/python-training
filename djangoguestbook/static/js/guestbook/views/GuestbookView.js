define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/request",
    "dojo/on",
    "dojo/dom",
    "dojo/dom-construct",
    "dojo/_base/array",
    "/static/js/guestbook/views/GreetingView.js",
    "/static/js/guestbook/views/SignFormWidget.js",
    "/static/js/guestbook/views/models/GreetingStore.js",
    "dojo/text!./templates/GuestbookView.html"
], function(declare, lang, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
            request, on, dom, domConstruct, arrayUtil, GreetingView, SignFormWidget,
            GreetingStore, template){
    return declare("guestbook.GuestbookView", [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
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
            var _isAdmin = "false";
            var isUserAdminNode = dom.byId("is_user_admin");
            if (isUserAdminNode){
                _isAdmin = isUserAdminNode.value;
            }

            var _userLogin = "false";
            var userLoginNode = dom.byId("user_login");
            if (userLoginNode){
                _userLogin = userLoginNode.value;
            }

            var _guestbookWidgetParent = this;

            var _greetingList = this.GreetingStore.getListGreeting(guestbookName);
            _greetingList.then(function(results){
                var _newDocFrag = document.createDocumentFragment();
                arrayUtil.forEach(results.greetings, function(greeting){
                    var greetingView = new GreetingView(greeting);
                    // show button delete for admin
                    if (_isAdmin.toLowerCase() == "true"){
                        greetingView.setHiddenDeleteNode(false);
                        greetingView.setDisabledEditor(false);
                    }
                    // show button edit if author written
                    if (_userLogin == greeting.author){
                        greetingView.setDisabledEditor(false);
                    }
                    // set guestbook name
                    greetingView.setGuestbookName(guestbookName);
                    greetingView.setGuestbookParent(_guestbookWidgetParent);

                    greetingView.placeAt(_newDocFrag);
                });
                domConstruct.place(_newDocFrag, _guestbookWidgetParent.greetingsContainerNode);
            }, function(err){
                console.log(err.message);
            }, function(progress){
                console.log(progress);
            });
        },

        _onclickSwitchBtn: function(){
            var _guestbookNameLength = this.guestbookNameNode.value;
            if (_guestbookNameLength > 0 && _guestbookNameLength <= 20){
                this.reloadListGreeting(this.guestbookNameNode.value);
                // set guestbook name for Sign form
                this.signFormWidget._setGuestbookNameAttr(this.guestbookNameNode.value);
            } else {
                alert("Error: Guestbook name is empty or length > 20 chars")
            }
        },

        _removeAllGreeting: function(){
            this.greetingsContainerNode.innerHTML = "";
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