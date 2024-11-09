import { MainLayout } from '../../components/layout';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { phishingApi } from '../../apis';
import { Button, Loader, ProgressCircle } from '../../components/common';

function HomePage() {
  const [urlInput, setUrlInput] = useState('');
  const [phishingMessage, setPhishingMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [phishingProbability, setPhishingProbability] = useState(-1);
  const [loading, setLoading] = useState(false);

  const handleCheckPhishing = async (e) => {
    e.preventDefault();

    if (!urlInput.trim()) return;

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
      } else {
        setPhishingMessage('Trang web kiểm tra có độ an toàn cao.');
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

  return (
    <MainLayout>
      <div className="py-8 sm:py-6">
        <div className="container px-5 sm:px-4">
          <h1 className="text-3xl sm:text-2xl text-primary font-bold text-center mb-3 animate-appear">
            Phát hiện trang web lừa đảo
          </h1>
          <p className="mb-5">
            Lưu ý: Công cụ của chúng tôi chỉ đưa ra dự đoán về khả năng một trang web có phải là lừa
            đảo hay không nhằm cảnh báo sớm cho người dùng mà chưa được xác minh một cách chính
            thức. Để biết thêm chi tiết hãy xem đầy đủ{' '}
            <Link className="text-secondary hover:underline" to="/">
              điều khoản
            </Link>{' '}
            và{' '}
            <Link className="text-secondary hover:underline" to="/">
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
                className="flex-1 outline-none border border-tertiary px-4 py-2 rounded-lg focus:border-secondary transition-all"
                type="text"
                placeholder="Nhập URL muốn kiểm tra..."
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
              />
              <Button title="Kiểm tra" type="submit" isDisable={!urlInput.trim()} />
            </form>
          </div>
          <div>
            {!loading ? (
              <>
                <ProgressCircle percentage={phishingProbability * 100} />
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
  );
}

export default HomePage;
