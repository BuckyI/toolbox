// ==UserScript==
// @name         Copy
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  在复制网页内容后，剪贴板内添加一行网页链接（会丢失格式）
// @author       You
// @match        *://*/*
// @grant        GM_registerMenuCommand
// ==/UserScript==

function addEvent() {
    document.addEventListener('copy', function (e) {
        var selection = window.getSelection();
        if (selection.rangeCount) {
            // create a new div element to contain the selected text and link
            var container = document.createElement('div');

            // get the selected range and clone it
            var range = selection.getRangeAt(0);
            var clonedRange = range.cloneRange();

            // wrap the cloned range in the new container div
            container.appendChild(clonedRange.cloneContents());

            // add the source link to the end of the copied text
            var pagelink = '<br/>-- [' + document.title + '](' + document.location.href + ')';
            container.innerHTML += pagelink;

            // serialize the HTML contents of the container div
            var serializedHtml = (new XMLSerializer()).serializeToString(container);

            // set the serialized HTML as the data to be copied to the clipboard
            e.clipboardData.setData('text/html', serializedHtml);

            // prevent the default copy behavior
            e.preventDefault();
        }
    });
}


(function () {
    'use strict';
    // addEvent();
    // 注册快捷键并关联回调函数
    GM_registerMenuCommand("复制添加网页链接", function () {
        addEvent();
        alert('现在开始，复制文字都会添加网页链接！');
    });
})();
