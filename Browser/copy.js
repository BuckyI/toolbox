// ==UserScript==
// @name         Copy
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  在复制网页内容后，剪贴板内添加一行网页链接（会丢失格式）
// @author       You
// @match        *://*/*
// @icon         
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    document.addEventListener('copy', function (e) {
        var selectionText = document.getSelection().toString();
        var pagelink = '-- [source](' + document.location.href + ')';
        var copyText = selectionText + '\r\n' + pagelink;
        e.clipboardData.setData('text/plain', copyText);
        e.preventDefault();
    });
})();


