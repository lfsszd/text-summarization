$(function(){
    $('#keywordsubmit').click(function(){
		chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
			chrome.tabs.executeScript(
				tabs[0].id,
				{ code: 'var s = document.documentElement.outerHTML; chrome.runtime.sendMessage({action: "getSource", source: s});' }
			);
		});
		chrome.runtime.sendMessage(
			{content: document.documentElement.innerHTML, action:"source"}
		);
	})
});
