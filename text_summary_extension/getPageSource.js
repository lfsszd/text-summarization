console.log('injected')
chrome.runtime.sendMessage({
    action: "summary",
    content: document.documentElement.outerHTML
},
function(response) {
    result = response;
    alert(result.summary);
    
});
