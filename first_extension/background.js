// 實作功能的主要的操作邏輯
chrome.runtime.onInstalled.addListener(async ()=> {
    const url = chrome.runtime.getURL('/popup/popup.html');
    const tab = await chrome.tabs.create({
        url 
    });
    console.log(`Create tab ${tab.id}`);
})
// // set object
// chrome.storage.sync.set({ 'status': 0 }).then(() => {
//     console.log("Value is set");
// });



// chrome.storage.onChanged.addListener((changes, namespace) => {
//     if (data.status == 0) {
//         chrome.browserAction.setPopup({ popup: 'popup.html' });
//       } else {
//         chrome.browserAction.setPopup({ popup: 'loading.html' });
//       }
//   });