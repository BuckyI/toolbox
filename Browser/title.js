// ==UserScript==
// @name         Mightymjolnir's Script
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @run-at       document-body
// @icon         https://www.google.com/s2/favicons?sz=64&domain=theb.ai
// @grant        none
// TODO 清洁标题的垃圾信息，一大串后缀之类的
// ==/UserScript==

function waitForTitleChange(originalTitle, timeout) {
    return new Promise((resolve, reject) => {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (const mutation of mutationsList) {
                if (mutation.type === 'childList' && document.title !== originalTitle) {
                    resolve(document.title);
                    document.title = originalTitle;
                    observer.disconnect();
                    return;
                }
            }
        });

        observer.observe(document.querySelector('head'), { childList: true });

        setTimeout(() => {
            observer.disconnect();
            reject(new Error('时间到了，标题应该不会被修改了吧'));
        }, timeout);
    });
}

(async function () {
    try {
        const originalTitle = document.title;
        console.log('读取到原标题', originalTitle);
        const title = await waitForTitleChange(originalTitle, 10000);
        console.log('读取到变更标题 ', title, '，已恢复原标题');
    } catch (error) {
        console.error(error.message);
    }
})();