import { MainLayout } from '../../components/layout';
import { Helmet } from 'react-helmet';

function PolicyPage() {
  return (
    <MainLayout>
      <Helmet>
        <title>PhishDetect.net - Chính sách bảo mật</title>
      </Helmet>
      <div className="py-8 sm:py-6">
        <div className="container px-5 sm:px-4">
          <div>
            <h1 className="text-3xl sm:text-2xl text-primary font-bold mb-3 animate-appear">
              Chính sách bảo mật
            </h1>
            <p className="text-sm">Chính sách bảo mật</p>
          </div>
          <div className="mt-20 md:mt-12 sm:mt-8">
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Thông tin chúng tôi thu thập</h2>
              <p className="mb-2 text-justify">
                <i>URL của trang web: </i> Khi người dùng nhập URL vào công cụ hoặc truy cập một
                trang web thông qua tiện ích, chúng tôi sẽ lấy URL này để phân tích. Việc phân tích
                bao gồm kiểm tra đặc điểm URL và nội dung trang để đánh giá các dấu hiệu rủi ro liên
                quan đến phishing.
              </p>
              <p className="text-justify">
                <i>Nội dung của trang web: </i>Chúng tôi cũng lấy nội dung của trang web ứng với URL
                tương ứng để hỗ trợ cho quá trình phân tích nhưng không lưu trữ hoặc sử dụng vào mục
                đích khác ngoài phát hiện phishing.
              </p>
            </div>
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Cách chúng tôi sử dụng dữ liệu</h2>
              <p className="mb-2 text-justify">
                <i>Chỉ sử dụng dữ liệu cần thiết: </i>Chúng tôi chỉ sử dụng URL và nội dung trang để
                xác định các dấu hiệu của phishing. Dữ liệu này giúp chúng tôi cung cấp cảnh báo kịp
                thời nếu trang web có dấu hiệu nguy hiểm.
              </p>
              <p className="text-justify">
                <i>Không thu thập và lưu trữ thông tin cá nhân: </i>Công cụ của chúng tôi hoạt động
                độc lập, không yêu cầu người dùng đăng nhập và không lưu trữ bất kỳ thông tin cá
                nhân nào khác ngoài URL và dữ liệu phân tích trong quá trình kiểm tra. Sau khi hoàn
                tất phân tích, các dữ liệu này sẽ bị xóa và không được giữ lại. Chúng tôi không lưu
                lại bất cứ lịch sử duyệt web nào của người dùng. Chúng tôi cũng cam kết không thu
                thập bất cứ dữ liệu cá nhân nào từ các trang web mà người dùng truy cập.
              </p>
            </div>
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">
                Cách chúng tôi xử lý khi phát hiện phishing
              </h2>
              <p className="text-justify">
                <i>Không can thiệp vào quá trình duyệt web: </i>Khi sử dụng tiện tích, chúng tôi chỉ
                đưa ra cảnh báo cho người dùng biết khi khả năng phishing của website đó vượt quá
                ngưỡng mà người dùng cài đặt. Chúng tôi cam kết không gây bất cứ tác động nào đến
                khả năng truy cập vào các website trên trình duyệt của người dùng. Tiện ích hoạt
                động một cách thụ động, chỉ đưa ra cảnh báo dưới dạng thông báo, để người dùng tự
                đưa ra quyết định cuối cùng về việc truy cập.
              </p>
            </div>
            <div className="py-10">
              <h2 className="text-xl font-medium mb-2">Thay đổi chính sách</h2>
              <p className="text-justify">
                <i>Cập nhật chính sách: </i>Chính sách quyền riêng tư có thể được thay đổi hoặc cập
                nhật theo thời gian. Mọi thay đổi sẽ được không được thông báo đến người dùng mà sẽ
                được cập nhật ngay trên website của chúng tôi và có hiệu lực ngay khi đăng tải.
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default PolicyPage;
