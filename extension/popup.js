document.addEventListener('DOMContentLoaded', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const isLocal =
    tab.url.startsWith('http://localhost') ||
    tab.url.startsWith('http://127.0.0.1') ||
    tab.url.startsWith('file://') ||
    /^http:\/\/192\.168\.\d+\.\d+/.test(tab.url) ||
    /^http:\/\/10\.\d+\.\d+\.\d+/.test(tab.url);

  const statusContainer = document.getElementById('statusContainer');

  if (isLocal) {
    statusContainer.innerHTML = `
        <div class="info-box">
            <span role="img" aria-label="Info" class="info-icon">ℹ️</span>
            <span id="phishingMessage">Bạn đang truy cập trang web nội bộ nên không cần kiểm tra lừa đảo.</span>
        </div>`;
    return;
  }

  chrome.storage.sync.get(['phishingThreshold', 'phishingData'], async (data) => {
    const threshold = data.phishingThreshold || 50;
    const currentUrl = data.phishingData?.url;
    const currentScore = data.phishingData?.score;

    if (currentUrl === tab.url) {
      displayPhishingScore(currentScore);
    } else {
      statusContainer.innerHTML = '<span class="loader"></span>';
      try {
        const response = await fetch(
          'https://phishing-model-api-app.icyrock-5c48d03b.southeastasia.azurecontainerapps.io/predict',
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url }),
          }
        );
        const result = await response.json();
        const phishingScore = Math.round(result.phishing_probability * 100);

        chrome.storage.sync.set({ phishingData: { url: tab.url, score: phishingScore } });
        displayPhishingScore(phishingScore);
      } catch (error) {
        console.error(error);
        displayPhishingScore(-1);
      }
    }

    updateThreshold(threshold);
    updateSafeCheckbox(tab.url);
  });

  function displayPhishingScore(phishingScore) {
    statusContainer.innerHTML = `
        <div class='progress-box'>
            <svg class="progress-circle" width="80" height="80" viewBox="0 0 80 80">
                <circle cx="40" cy="40" r="36" stroke-width="8" class="progress-bg" fill="none"></circle>
                <circle cx="40" cy="40" r="36" stroke-width="8" fill="none" class="progress-bar"></circle>
            </svg>
            <span id="percentageText" class="percentage-text">N/A</span>
        </div>
        <div class="info-box">
            <span role="img" aria-label="Info" class="info-icon">ℹ️</span>
            <span id="phishingMessage">Không xác định.</span>
        </div>`;
    updatePhishing(phishingScore);
  }

  function updateThreshold(threshold) {
    const thresholdLabel = document.getElementById('thresholdLabel');
    const labelText = thresholdLabel.querySelector('span');
    const toggleIcon = thresholdLabel.querySelector('img');
    const thresholdAdjust = document.getElementById('thresholdAdjust');
    const thresholdInput = document.getElementById('threshold');
    const decreaseButton = document.getElementById('decreaseThreshold');
    const increaseButton = document.getElementById('increaseThreshold');

    labelText.textContent = `Ngưỡng cảnh báo: ${threshold}`;
    thresholdInput.value = threshold;

    thresholdLabel.addEventListener('click', () => {
      thresholdAdjust.classList.toggle('hidden');
      chrome.storage.sync.get('phishingThreshold', (data) => {
        currentThreshold = data.phishingThreshold || 50;
        if (thresholdAdjust.classList.contains('hidden')) {
          labelText.textContent = `Ngưỡng cảnh báo: ${currentThreshold}`;
          toggleIcon.src = './assets/arrow-right.svg';
        } else {
          labelText.textContent = 'Ngưỡng cảnh báo';
          toggleIcon.src = './assets/arrow-bottom.svg';
        }
      });
    });

    thresholdInput.addEventListener('change', () => {
      const newThreshold = Math.min(Math.max(thresholdInput.value, 0), 100);
      thresholdInput.value = newThreshold;
      chrome.storage.sync.set({ phishingThreshold: newThreshold });
    });

    decreaseButton.addEventListener('click', () => {
      thresholdInput.value = Math.max(+thresholdInput.value - 1, 0);
      thresholdInput.dispatchEvent(new Event('change'));
    });

    increaseButton.addEventListener('click', () => {
      thresholdInput.value = Math.min(+thresholdInput.value + 1, 100);
      thresholdInput.dispatchEvent(new Event('change'));
    });
  }

  function updateSafeCheckbox(url) {
    const safeCheckbox = document.getElementById('safeCheckbox');
    const domain = new URL(url).hostname;

    chrome.storage.sync.get({ safeDomainList: [] }, (data) => {
      const safeDomainList = data.safeDomainList || [];
      safeCheckbox.checked = safeDomainList.includes(domain);
    });

    safeCheckbox.addEventListener('change', () => {
      chrome.storage.sync.get({ safeDomainList: [] }, (data) => {
        let safeDomainList = data.safeDomainList || [];

        if (safeCheckbox.checked) {
          if (!safeDomainList.includes(domain)) {
            safeDomainList.push(domain);
          }
        } else {
          safeDomainList = safeDomainList.filter((item) => item !== domain);
        }

        chrome.storage.sync.set({ safeDomainList });
      });
    });
  }

  function updatePhishing(percentage) {
    const progressCircle = document.querySelector('.progress-bar');
    const percentageText = document.getElementById('percentageText');
    const phishingMessage = document.getElementById('phishingMessage');

    const strokeWidth = 8;
    const radius = (80 - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const progress = percentage > 0 ? circumference * (1 - percentage / 100) : 0;

    progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
    progressCircle.style.strokeDashoffset = progress;

    if (percentage > 75) {
      progressCircle.classList.add('stroke-red');
      phishingMessage.textContent = 'Nguy cơ lừa đảo cao.';
    } else if (percentage > 50) {
      progressCircle.classList.add('stroke-orange');
      phishingMessage.textContent = 'Có khả năng lừa đảo.';
    } else if (percentage > 25) {
      progressCircle.classList.add('stroke-yellow');
      phishingMessage.textContent = 'Có khả năng an toàn.';
    } else if (percentage >= 0) {
      progressCircle.classList.add('stroke-green');
      phishingMessage.textContent = 'Mức độ an toàn cao.';
    } else {
      progressCircle.classList.add('stroke-gray');
      phishingMessage.textContent = 'Không xác định.';
    }

    percentageText.textContent = percentage >= 0 ? `${percentage}%` : 'N/A';
  }
});
