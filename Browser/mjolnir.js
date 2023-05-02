// ==UserScript==
// @name         mjolnir
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  useful tools for browser
// @author       Thor
// @match        *://*/*
// @grant        GM_registerMenuCommand
// ==/UserScript==

function processClipboard(e) {
    /** 
     * Processes the clipboard event and copies the selected text and source link to the clipboard
     * @param {object} e - The clipboard event object 
     */
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
}

function modifyTitle() {
    /**
     * Modify the title of the document by removing specific patterns from it.
     */
    var title = document.title;
    const regexes = [
        [/^\(\d+ 封私信 \/ \d+ 条消息\)/, ''],
        [/^\(\d+ 封私信\)/, ''],
        [/_哔哩哔哩_bilibili/, ' - 哔哩哔哩'],
        [/_.*$/, '']
    ];

    for (const [match, target] of regexes) {
        title = title.replace(match, target);
    }

    console.log("title modified:\nfrom:", document.title, "\nto:", title);
    document.title = title;
}

(function () {
    'use strict';

    setTimeout(modifyTitle, 10000);

    // 注册快捷键并关联回调函数
    GM_registerMenuCommand("复制添加网页链接", function () {
        document.addEventListener('copy', processClipboard);
        alert('现在开始，复制文字都会添加网页链接！');
    });
    GM_registerMenuCommand("停用", function () {
        document.removeEventListener('copy', processClipboard);
        alert('已停用 EventListener ');
    });
})();
