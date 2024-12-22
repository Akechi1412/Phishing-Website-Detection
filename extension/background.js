chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const isLocal =
      tab.url.startsWith('http://localhost') ||
      tab.url.startsWith('http://127.0.0.1') ||
      tab.url.startsWith('file://') ||
      /^http:\/\/192\.168\.\d+\.\d+/.test(tab.url) ||
      /^http:\/\/10\.\d+\.\d+\.\d+/.test(tab.url);
    const isResource =
      /\.(jpg|jpeg|png|gif|svg|bmp|webp|mp4|mp3|wav|pdf|doc|docx|ppt|pptx|xls|xlsx)$/i.test(
        tab.url
      );
    if (isLocal || isResource) return;

    try {
      const apiUrl = 'http://localhost:8000/predict';
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: tab.url,
        }),
      });
      const result = await response.json();
      const phishingScore = Math.round(result.phishing_probability * 100);
      chrome.storage.sync.set({ phishingData: { url: tab.url, score: phishingScore } });
      chrome.action.setBadgeText({ text: `${phishingScore >= 0 ? phishingScore : 'N/A'}` });
      let badgeColor = '#e5e7eb';
      if (phishingScore >= 75) {
        badgeColor = '#f87171';
      } else if (phishingScore >= 50) {
        badgeColor = '#fb923c';
      } else if (phishingScore >= 25) {
        badgeColor = '#facc15';
      } else if (phishingScore >= 0) {
        badgeColor = '#34d399';
      }
      chrome.action.setBadgeBackgroundColor({ color: badgeColor });

      chrome.storage.sync.get(['safeDomainList', 'phishingThreshold'], (data) => {
        const safeDomainList = data.safeDomainList;
        const domain = new URL(tab.url).hostname;
        if ((safeDomainList ?? []).includes(domain)) {
          chrome.action.setBadgeText({ text: '' });
          return;
        }

        phishingThreshold = data.phishingThreshold || 50;
        if (phishingScore >= phishingThreshold) {
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
