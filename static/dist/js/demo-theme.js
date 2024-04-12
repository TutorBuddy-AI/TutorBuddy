/*!
* Xdialer v1.0.0-beta19 (https://xdialer.io)
* @version 1.0.0-beta19
* @link https://xdialer.io
* Copyright 2018-2023 The Xdialer Authors
* Copyright 2018-2023 xdialer.net xdialer
* Licensed under MIT (https://github.com/xdialer/xdialer/blob/master/LICENSE)
*/
(function (factory) {
	typeof define === 'function' && define.amd ? define(factory) :
	factory();
})((function () { 'use strict';

	var themeStorageKey = "xdialerTheme";
	var defaultTheme = "light";
	var selectedTheme;
	var params = new Proxy(new URLSearchParams(window.location.search), {
	  get: function get(searchParams, prop) {
	    return searchParams.get(prop);
	  }
	});
	if (!!params.theme) {
	  localStorage.setItem(themeStorageKey, params.theme);
	  selectedTheme = params.theme;
	} else {
	  var storedTheme = localStorage.getItem(themeStorageKey);
	  selectedTheme = storedTheme ? storedTheme : defaultTheme;
	}
	if (selectedTheme === 'dark') {
	  document.body.setAttribute("data-bs-theme", selectedTheme);
	} else {
	  document.body.removeAttribute("data-bs-theme");
	}

}));
