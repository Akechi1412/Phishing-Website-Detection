chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    try {
      const response = await fetch(
        'https://phishing-model-api-app.icyrock-5c48d03b.southeastasia.azurecontainerapps.io/predict',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            url: tab.url,
          }),
        }
      );
      const result = await response.json();
      const phishingScore = Math.round(result.phishing_probability * 100);
      chrome.storage.sync.set({ phishingData: { url: tab.url, score: phishingScore } });

      chrome.storage.sync.get(['safeDomainList', 'phishingThreshold'], (data) => {
        const safeDomainList = data.safeDomainList;
        const domain = new URL(tab.url).hostname;
        if ((safeDomainList ?? []).includes(domain)) return;

        phishingThreshold = data.phishingThreshold || 50;
        if (phishingScore > phishingThreshold) {
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'assets/icon48.png',
            title: 'Cảnh báo trang web lừa đảo',
            message: `Trang web ${tab.url} có ${phishingScore}% khả năng là trang web lừa đảo. Hãy cẩn thận khi cung cấp các thông tin nhạy cảm.`,
          });
        }
      });
    } catch (error) {
      console.log(error);
    }
  }
});
