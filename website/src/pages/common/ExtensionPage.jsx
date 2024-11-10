import { MainLayout } from '../../components/layout';

function ExtensionPage() {
  document.title = 'PhishDetect - Extension cho trình duyệt';

  return (
    <MainLayout>
      <div className="py-8 sm:py-6">
        <div className="container mx-auto px-5 sm:px-4">
          <h1 className="text-3xl sm:text-2xl text-primary font-bold text-center mb-6 animate-appear-from-left">
            PhishDetect - Công cụ bảo vệ bạn khỏi các trang web lừa đảo
          </h1>
          <p className="mb-5">
            PhishDetect là extension giúp bạn phát hiện và tránh các trang web lừa đảo khi duyệt
            web. Với công nghệ AI, PhishDetect có thể phân tích các trang web và đưa ra cảnh báo nếu
            phát hiện rủi ro lừa đảo.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-1 gap-6">
            <div className="bg-tertiary/20 rounded-lg shadow-lg p-5 text-center animate-appear-from-left">
              <h2 className="text-xl font-semibold text-secondary mb-2">
                Cảnh báo trang web lừa đảo
              </h2>
              <p className="text-gray-600">
                PhishDetect sẽ tự động kiểm tra URL bạn truy cập và đưa ra cảnh báo nếu phát hiện
                nguy cơ lừa đảo. Ngoài ra có thể xem phầm trăm khả năng trang web đó là trang web
                lừa đảo.
              </p>
            </div>
            <div className="bg-tertiary/20 rounded-lg shadow-lg p-5 text-center animate-appear-from-right">
              <h2 className="text-xl font-semibold text-secondary mb-2">
                Điều chỉnh ngưỡng cảnh báo
              </h2>
              <p className="text-gray-600">
                Bạn có thể tùy chỉnh ngưỡng cảnh báo, chọn mức độ nhạy cảm với các trang web nghi
                ngờ lừa đảo để phù hợp với nhu cầu cá nhân.
              </p>
            </div>
            <div className="bg-tertiary/20 rounded-lg shadow-lg p-5 text-center animate-appear-from-left">
              <h2 className="text-xl font-semibold text-secondary">Đánh dấu trang web an toàn</h2>
              <p className="text-gray-600">
                Do là công cụ AI nên có thể sẽ có nhầm lẫn khi phát hiện trang web phishing. Do đó
                với các trang mà bạn tin tưởng, bạn có thể đánh dấu là an toàn để không nhận cảnh
                báo mỗi khi truy cập vào các trang này.
              </p>
            </div>
            <div className="bg-tertiary/20 rounded-lg shadow-lg p-5 text-center animate-appear-from-right">
              <h2 className="text-xl font-semibold text-secondary mb-2">Trình duyệt hỗ trợ</h2>
              <p className="text-gray-600">
                Hiện tại extension của chúng tôi chỉ hỗ trợ trên trình duyệt Chrome. Tuy nhiên do
                chưa có trên store nên bạn có thể tự cài đặt với mã nguồn mở{' '}
                <a
                  className="text-secondary hover:underline transition-all"
                  href="https://github.com/Akechi1412/Phishing-Website-Detection/tree/main/extension"
                  target="_blank"
                >
                  tại đây
                </a>
                .
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default ExtensionPage;
