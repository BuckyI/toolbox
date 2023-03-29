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
    setTimeout(function () {
        document.title = originalTitle;
        // 输出调试信息
        console.log('原始标题：', originalTitle);
    }, 5000); // 5 秒后执行
})();