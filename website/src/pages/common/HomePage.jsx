import { MainLayout } from '../../components/layout';
import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { phishingApi } from '../../apis';
import { Button, Loader, ProgressCircle } from '../../components/common';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import ReCAPTCHA from 'react-google-recaptcha';

function HomePage() {
  const siteKey = import.meta.env.PD_CAPCHA_SITE_KEY;
  const [urlInput, setUrlInput] = useState('');
  const [phishingMessage, setPhishingMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [phishingProbability, setPhishingProbability] = useState(-1);
  const [loading, setLoading] = useState(false);
  const [submitCount, setSubmitCount] = useState(0);
  const [showCaptcha, setShowCaptcha] = useState(false);
  const [captchaVerified, setCaptchaVerified] = useState(false);
  const [captchaExpired, setCaptchaExpired] = useState(false);

  const handleCheckPhishing = async (e) => {
    e.preventDefault();

    if (showCaptcha) {
      setShowCaptcha(false);
      setCaptchaVerified(false);
      sessionStorage.setItem('submitCount', '0');
      setSubmitCount(0);
    } else {
      if (submitCount >= 2 && !captchaVerified) {
        setShowCaptcha(true);
        return;
      }
      const newCount = submitCount + 1;
      sessionStorage.setItem('submitCount', newCount.toString());
      setSubmitCount(newCount);
    }
    setPhishingMessage('');
    setErrorMessage('');
    setLoading(true);
    try {
      const data = await phishingApi.predict({ url: urlInput });
      const probability = data.phishing_probability;
      setPhishingProbability(probability);
      if (probability > 0.75) {
        setPhishingMessage('Trang web kiểm tra có nguy cơ lừa đảo cao. Hãy cẩn thận khi truy cập.');
      } else if (probability > 0.5) {
        setPhishingMessage(
          'Trang web kiểm tra có khả năng là lừa đảo. Hãy chú ý trước khi cung cấp bất kỳ thông tin nhạy cảm nào.'
        );
      } else if (probability > 0.25) {
        setPhishingMessage('Trang web kiểm tra có khả năng là an toàn.');
      } else if (probability >= 0) {
        setPhishingMessage('Trang web kiểm tra có độ an toàn cao.');
      } else {
        setPhishingMessage(
          'Không xác định do trang web từ URL bạn nhập vào có thể không có định dạng text/html.'
        );
      }
      setLoading(false);
    } catch (error) {
      setPhishingProbability(-1);
      setLoading(false);
      if (error.status === 400) {
        setErrorMessage(
          'URL sai hoặc trang web không thể truy cập hoặc trang web không còn tồn tại.'
        );
      } else if (error.status === 408) {
        setErrorMessage('Mất quá nhiều thời gian để truy cập vào URL.');
      } else {
        setErrorMessage('Có lỗi gì đó xảy ra. Vui lòng thử lại.');
      }
    }
  };

  const handleCaptchaChange = (value) => {
    if (value) {
      setCaptchaVerified(true);
      setCaptchaExpired(false);
    }
  };

  const handleCaptchaExpired = () => {
    setCaptchaVerified(false);
    setCaptchaExpired(true);
  };

  useEffect(() => {
    const count = parseInt(sessionStorage.getItem('submitCount')) || 0;
    setSubmitCount(count);
  }, []);

  return (
    <HelmetProvider>
      <MainLayout>
        <Helmet>
          <title>PhishDetect.net - Công cụ phát hiện trang web lừa đảo</title>
          <meta
            name="description"
            content="PhishDetect.net giúp bạn kiểm tra và bảo vệ khỏi các trang web lừa đảo bằng cách sử dụng công nghệ AI tiên tiến."
          />
          <meta name="robots" content="index, follow" />
          <meta
            name="keywords"
            content="phishing, lừa đảo, bảo mật, phát hiện lừa đảo, phát hiện phishing, cảnh báo lừa đảo, cảnh báo phishing, kiểm tra trang web an toàn"
          />
          <meta
            property="og:title"
            content="PhishDetect.net - Công cụ phát hiện trang web lừa đảo"
          />
          <meta
            property="og:description"
            content="Phát hiện và cảnh báo người dùng về các trang web lừa đảo tiềm ẩn với công nghệ phát hiện tiên tiến."
          />
          <meta property="og:image" content="https://phishdetect.net/phish_detect.png" />
          <meta property="og:url" content="https://phishdetect.net/" />
          <meta property="og:type" content="website" />
        </Helmet>
        <div className="py-8 sm:py-6">
          <div className="container px-5 sm:px-4">
            <h1 className="text-3xl sm:text-2xl text-primary font-bold text-center mb-3 animate-appear">
              Phát hiện trang web lừa đảo
            </h1>
            <p className="mb-5">
              Lưu ý: Công cụ của chúng tôi chỉ đưa ra dự đoán về khả năng một trang web có phải là
              lừa đảo hay không nhằm cảnh báo sớm cho người dùng mà chưa được xác minh một cách
              chính thức. Để biết thêm chi tiết hãy xem đầy đủ{' '}
              <Link className="text-secondary hover:underline" to="/terms">
                điều khoản
              </Link>{' '}
              và{' '}
              <Link className="text-secondary hover:underline" to="/policy">
                chính sách
              </Link>{' '}
              của chúng tôi.
            </p>
            <div className="flex justify-center mb-5">
              <form
                onSubmit={handleCheckPhishing}
                className="w-[600px] max-w-full flex space-x-3 sm:space-x-0 sm:space-y-4 sm:flex-col"
              >
                <input
                  className={`flex-1 outline-none border border-tertiary px-4 py-2 rounded-lg focus:border-secondary transition-all${
                    loading ? ' cursor-not-allowed' : ''
                  }`}
                  type="text"
                  placeholder="Nhập URL muốn kiểm tra..."
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  disabled={loading}
                  name="url"
                />
                <Button
                  title="Kiểm tra"
                  type="submit"
                  isDisable={
                    !urlInput.trim() ||
                    loading ||
                    (showCaptcha && (!captchaVerified || captchaExpired))
                  }
                />
              </form>
            </div>
            {showCaptcha && (
              <div className="flex justify-center mb-5">
                <ReCAPTCHA
                  sitekey={siteKey}
                  onChange={handleCaptchaChange}
                  onExpired={handleCaptchaExpired}
                />
              </div>
            )}
            <div>
              {!loading ? (
                <>
                  <ProgressCircle percentage={Math.round(phishingProbability * 100)} />
                  {phishingMessage && (
                    <div className="mt-4 flex justify-center">
                      <p className="text-center px-4 py-2 bg-primary/10 border-l-4 border-primary text-primary font-medium shadow-md rounded-md transition-transform duration-300 ease-in-out transform hover:scale-105">
                        <span role="img" aria-label="Info" className="mr-2">
                          ℹ️
                        </span>
                        {phishingMessage}
                      </p>
                    </div>
                  )}

                  {errorMessage && (
                    <div className="mt-4 flex justify-center">
                      <p className="text-center px-4 py-2 bg-red-100 border-l-4 border-red-500 text-red-500 font-medium shadow-md rounded-md transition-transform duration-300 ease-in-out transform hover:scale-105">
                        <span role="img" aria-label="Error" className="mr-2">
                          🚫
                        </span>
                        {errorMessage}
                      </p>
                    </div>
                  )}
                </>
              ) : (
                <Loader />
              )}
            </div>
          </div>
        </div>
      </MainLayout>
    </HelmetProvider>
  );
}

export default HomePage;
