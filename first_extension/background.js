// 實作功能的主要的操作邏輯
chrome.runtime.onInstalled.addListener(async ()=> {
    const url = chrome.runtime.getURL('popup.html');
    const tab = await chrome.tabs.create({
        url 
    });
    console.log(`Create tab ${tab.id}`);
})