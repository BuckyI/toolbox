// ==UserScript==
// @name         mjolnir
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  useful tools for browser, https://github.com/BuckyI/toolbox
// @author       Thor
// @match        *://*/*
// @grant        GM_registerMenuCommand
// @grant        GM_notification
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
        [/^\(\d+\)/, ''],
        [/-腾讯云开发者社区 - 腾讯云开发者社区/, ''],
        [/_哔哩哔哩_bilibili/, ' - 哔哩哔哩'],
        [/(_.*?){1,2}-CSDN博客$/, ' - CSDN'],
        [/_[^\W]+$/, '']
    ];

    for (const [match, target] of regexes) {
        title = title.replace(match, target);
    }

    var isChanged = document.title !== title;
    if (isChanged) {
        console.log("title modified:\nfrom:", document.title, "\nto:", title);
        document.title = title;
    }
    return isChanged;
}


function blockKeyboardShortcuts(event) {
    /**
     * Block keyboard shortcuts.
     */
    const websites = ['app.capacities.io', 'v.flomoapp.com'];
    var current = window.location.hostname;
    if (websites.includes(current)) {
        console.log(`${current} 在匹配列表中，将禁用部分快捷键`);
        // 如果用户按下了 Ctrl + S 或 Command + S （Mac OS 快捷键），则阻止浏览器默认行为
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
        }
    }

}

function notification(text, title = 'Notification') {
    GM_notification({
        text: text,
        title: title,
        timeout: 1000,
        silent: true
    });
}


(function () {
    'use strict';
    let intervalId = setInterval(modifyTitle, 1000);
    setTimeout(() => clearInterval(intervalId), 10000);


    // 默认启用功能
    document.addEventListener('keydown', blockKeyboardShortcuts);
    // 注册快捷键并关联回调函数
    GM_registerMenuCommand("复制添加网页链接", function () {
        document.addEventListener('copy', processClipboard);
        notification('现在开始，复制文字都会添加网页链接！');
    });
    GM_registerMenuCommand("屏蔽快捷键[默认开启]", function () {
        document.addEventListener('keydown', blockKeyboardShortcuts);
        notification('屏蔽 ctrl+s!');
    });
    // 禁用功能
    GM_registerMenuCommand("停用", function () {
        document.removeEventListener('copy', processClipboard);
        document.removeEventListener('keydown', blockKeyboardShortcuts);
        notification("已停用所有的 EventListener");
    });

    console.log(window.window.location.hostname);
    console.log(window.window.location.href);
})();
