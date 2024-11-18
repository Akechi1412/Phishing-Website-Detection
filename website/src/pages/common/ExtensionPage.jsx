import { MainLayout } from '../../components/layout';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import Chrome from '../../assets/chrome.png';

function ExtensionPage() {
  const chromeExtensionUrl = import.meta.env.PD_CHROME_EXTENSION_URL;

  return (
    <HelmetProvider>
      <MainLayout>
        <Helmet>
          <title>PhishDetect.net - Tiện ích phát hiện trang web lừa đảo cho trình duyệt</title>
          <meta
            name="description"
            content="PhishDetect.net giúp bạn kiểm tra và bảo vệ khỏi các trang web lừa đảo bằng cách sử dụng công nghệ AI tiên tiến."
          />
          <meta name="robots" content="index, follow" />
          <meta
            name="keywords"
            content="phishing, lừa đảo, bảo mật, phát hiện lừa đảo, phát hiện phishing, cảnh báo lừa đảo, cảnh báo phishing, kiểm tra trang web an toàn, extension, tiện ích"
          />
          <meta
            property="og:title"
            content="PhishDetect.net - Tiện ích phát hiện trang web lừa đảo cho trình duyệt"
          />
          <meta
            property="og:description"
            content="Phát hiện vàc cảnh báo người dùng về các trang web lừa đảo tiềm ẩn với công nghệ phát hiện tiên tiến."
          />
          <meta property="og:image" content="https://phishdetect.net/phish_detect.png" />
          <meta property="og:url" content="https://phishdetect.net/extension" />
          <meta property="og:type" content="website" />
        </Helmet>
        <div className="py-8 sm:py-6">
          <div className="container mx-auto px-5 sm:px-4">
            <h1 className="text-3xl sm:text-2xl text-primary font-bold text-center mb-6 animate-appear-from-left">
              Tiện ích bảo vệ bạn khỏi các trang web lừa đảo
            </h1>
            <p>
              PhishDetect.net là extension giúp bạn phát hiện và tránh các trang web lừa đảo khi
              duyệt web. Với công nghệ AI, PhishDetect.net có thể phân tích các trang web và đưa ra
              cảnh báo nếu phát hiện rủi ro lừa đảo.
            </p>
            <div className="my-5">
              <div className="flex justify-center">
                <a
                  href={chromeExtensionUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 px-8 py-4 text-white font-semibold bg-gradient-to-r from-secondary to-primary rounded-full shadow-lg
                   hover:shadow-[0_0_15px_#5c94c3,0_0_30px_#5c94c3] transition-shadow duration-300 ease-in-out 
                   focus:outline-none focus:ring-4 focus:ring-tertiary"
                >
                  <img className="w-8 h-8" src={Chrome} alt="Chrome" />
                  <span className="tracking-wide">Cài đặt tiện ích trên Chrome Web Store</span>
                </a>
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-1 gap-6">
              <div className="bg-tertiary/15 rounded-lg shadow-lg p-5 text-center animate-appear-from-left">
                <h2 className="text-xl font-semibold text-secondary mb-2">
                  Cảnh báo trang web lừa đảo
                </h2>
                <p className="text-gray-600">
                  PhishDetect.net sẽ tự động kiểm tra URL bạn truy cập và đưa ra cảnh báo nếu phát
                  hiện nguy cơ lừa đảo. Ngoài ra có thể xem phầm trăm khả năng trang web đó là trang
                  web lừa đảo.
                </p>
              </div>
              <div className="bg-tertiary/15 rounded-lg shadow-lg p-5 text-center animate-appear-from-right">
                <h2 className="text-xl font-semibold text-secondary mb-2">
                  Điều chỉnh ngưỡng cảnh báo
                </h2>
                <p className="text-gray-600">
                  Bạn có thể tùy chỉnh ngưỡng cảnh báo, chọn mức độ nhạy cảm với các trang web nghi
                  ngờ lừa đảo để phù hợp với nhu cầu cá nhân.
                </p>
              </div>
              <div className="bg-tertiary/15 rounded-lg shadow-lg p-5 text-center animate-appear-from-left">
                <h2 className="text-xl font-semibold text-secondary mb-2">
                  Đánh dấu trang web an toàn
                </h2>
                <p className="text-gray-600">
                  Do là công cụ AI nên có thể sẽ có nhầm lẫn khi phát hiện trang web phishing. Do đó
                  với các trang mà bạn tin tưởng, bạn có thể đánh dấu là an toàn để không nhận cảnh
                  báo mỗi khi truy cập vào các trang này.
                </p>
              </div>
              <div className="bg-tertiary/15 rounded-lg shadow-lg p-5 text-center animate-appear-from-right">
                <h2 className="text-xl font-semibold text-secondary mb-2">Trình duyệt hỗ trợ</h2>
                <p className="text-gray-600">
                  Hiện tại extension của chúng tôi hỗ trợ trên trình duyệt Chrome và các trình duyệt
                  dựa trên Chromium như Microsoft Edge, Brave và Opera. Chúng tôi sẽ liên tục phát
                  triển để hỗ trợ nhiều trình duyệt hơn.
                </p>
              </div>
            </div>
          </div>
        </div>
      </MainLayout>
    </HelmetProvider>
  );
}

export default ExtensionPage;
