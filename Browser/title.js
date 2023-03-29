// ==UserScript==
// @name         Mightymjolnir's Script
// @namespace    http://tampermonkey.net/
// @version      0.1
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

    var loopCount = 0;
    var intervalId = setInterval(function () {
        loopCount++;
        if (loopCount >= 10) { // 循环达到10s后自动退出
            clearInterval(intervalId);
            console.log('已超时，未发现标题变化');
            return;
        }
        if (document.title !== originalTitle) { // 标题已经被修改
            document.title = originalTitle;
            clearInterval(intervalId);
            console.log('标题已恢复为原始标题：', originalTitle);
        }
    }, 1000); // 每隔1秒执行一次循环
})();