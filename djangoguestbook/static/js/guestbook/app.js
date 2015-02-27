define([
		'dojo/_base/config',
		'dojo/_base/window',
		'dojo/parser',
		'dojo/ready',
		'./views/GuestbookView'
], function(config, win, parser, ready, GuestbookView) {
		ready(function() {
			if (!config.parseOnLoad) {
				parser.parse();
			}
			var view = new GuestbookView(),
				body = win.body();
			view.placeAt(body);
			view.startup();
		});
});