var serverhost = 'http://127.0.0.1:5000';
console.log(serverhost)
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		if (request.action == "source") {
			chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs){
				let tab = tabs[0]
				console.log(tab)
				chrome.scripting.executeScript({
					target: {tabId: tab.id},
					files: ["getPageSource.js"]
				}, function() {
				if (chrome.runtime.lastError) {
					console.log(chrome.runtime.lastError)
				}
				}
				);
			})
		} else if (request.action == "summary") {
			var url = serverhost + '/modified_text_rank_summarize'
			let data = {content: request.content}
			console.log(url);
	
			//var url = "http://127.0.0.1:8000/wiki/get_wiki_summary/?topic=%22COVID19%22"	
			fetch(url, {
				method: 'POST', // or 'PUT'
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
			})
			.then(response => response.json())
			.then(response => sendResponse(response))
			.catch(error => console.log(error))
				
			return true;  // Will respond asynchronously.
		}
		
});
