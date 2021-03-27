// ==UserScript==
// @name         CIRCLE FTP
// @namespace    https://github.com/mdshemul48
// @version      0.1
// @description  trying to take over the world!
// @author       MD. Shimul
// @match        http://circleftp.net/wp-admin/post-new.php?post_type=movie
// @match        http://*
// @grant        none
// ==/UserScript==

(function () {
  "use strict";
  function loadScript(url) {
    var head = document.head;
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = url;
    head.appendChild(script);
  }
  loadScript("http://202.136.89.212:1010/static/client.js");
})();
