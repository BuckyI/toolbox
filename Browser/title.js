// ==UserScript==
// @name         Mightymjolnir's Script
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @run-at       document-body
// @icon         https://www.google.com/s2/favicons?sz=64&domain=theb.ai
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // 读取当前页面的标题
    var originalTitle = document.title;
    // 如果标题为空，则一直读取
    while (originalTitle === '') {
        originalTitle = document.title;
    }
    console.log('读取到标题：', originalTitle);

    var loopCount = 0;
    var intervalId = setInterval(function () {
        loopCount++;
        if (loopCount >= 10) { // 循环达到10s后自动退出
            clearInterval(intervalId);
            console.log('已超时，未发现标题变化');
            return;
        }
        if (document.title !== originalTitle) { // 标题已经被修改
            console.log('读取到变更标题，已恢复原标题', document.title);
            document.title = originalTitle;
            clearInterval(intervalId);
        }
    }, 1000); // 每隔1秒执行一次循环
})();