import { MainLayout } from '../../components/layout';
import { Helmet } from 'react-helmet';

function TermsPage() {
  return (
    <MainLayout>
      <Helmet>
        <title>PhishDetect.net - Điều khoản sử dụng</title>
      </Helmet>
      <div className="py-8 sm:py-6">
        <div className="container px-5 sm:px-4">
          <div>
            <h1 className="text-3xl sm:text-2xl text-primary font-bold mb-3 animate-appear">
              Điều khoản sử dụng
            </h1>
            <p className="text-sm">Điều khoản sử dụng</p>
          </div>
          <div className="mt-20 md:mt-12 sm:mt-8">
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Giới thiệu chung</h2>
              <p className="mb-2 text-justify">
                <i>Tổng quan về dịch vụ: </i> Công cụ và tiện ích phát hiện lừa đảo (phishing) của
                chúng tôi được thiết kế nhằm giúp người dùng phát hiện và phòng tránh các trang web
                có dấu hiệu lừa đảo. Dựa trên các thuật toán AI phân tích URL và đặc trưng của trang
                web, công cụ sẽ đưa ra các cảnh báo sớm nhằm giảm thiểu rủi ro và hỗ trợ người dùng
                bảo vệ thông tin cá nhân.
              </p>
              <p className="text-justify">
                <i>Phạm vi hỗ trợ: </i>Công cụ hoạt động như một lớp phòng ngừa bổ sung, giúp nâng
                cao cảnh giác khi truy cập vào các trang web nghi ngờ. Mặc dù công cụ được xây dựng
                với độ chính xác cao nhưng chúng tôi không thể cam kết kết quả hoàn toàn chính xác
                trong mọi tình huống và khuyến nghị người dùng phối hợp với các biện pháp an toàn
                khác.
              </p>
            </div>
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Phạm vi dịch vụ</h2>
              <p className="mb-2 text-justify">
                <i>Cách hoạt động: </i>Khi người dùng nhập URL ở website hoặc truy cập trang web qua
                tiện ích, công cụ sẽ phân tích và cung cấp đánh giá rủi ro. Nếu phát hiện dấu hiệu
                nghi ngờ, công cụ sẽ đưa ra cảnh báo trực quan, giúp người dùng cân nhắc về tính an
                toàn của trang.
              </p>
              <p className="text-justify">
                <i>Giới hạn và khuyến nghị: </i>Công cụ này mang tính chất hỗ trợ cảnh báo, không
                thay thế cho các phương pháp xác minh chuyên sâu. Chúng tôi khuyến cáo người dùng
                chỉ sử dụng công cụ như một nguồn tham khảo bổ sung và luôn thực hiện các biện pháp
                bảo mật bổ sung nếu cần thiết.
              </p>
            </div>
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Tránh nhiệm của người dùng</h2>
              <p className="mb-2 text-justify">
                <i>Độc lập xác minh: </i>Mặc dù công cụ đưa ra cảnh báo, quyết định cuối cùng về
                việc truy cập hoặc không truy cập một trang web, cung cấp thông tin gì ở trang web
                đó hoàn toàn thuộc quyền người dùng. Người dùng có trách nhiệm tự xem xét và đưa ra
                quyết định dựa trên nhiều nguồn thông tin.
              </p>
              <p className="text-justify">
                <i>Tuân thủ khuyến nghị: </i>Công cụ và tiện ích đưa ra các đánh giá rủi ro dựa trên
                dữ liệu có sẵn, nhưng không thể bao quát mọi tình huống. Do đó, người dùng đồng ý
                rằng mọi hành động sau khi nhận cảnh báo từ công cụ là tự nguyện và nằm ngoài trách
                nhiệm của chúng tôi.
              </p>
            </div>
            <div className="py-10 border-b border-b-tertiary">
              <h2 className="text-xl font-medium mb-2">Giới hạn trách nhiệm</h2>
              <p className="mb-2 text-justify">
                <i>Miễn trừ trách nhiệm: </i>Chúng tôi không chịu trách nhiệm đối với bất kỳ thiệt
                hại nào, dù là tổn thất dữ liệu, mất mát tài chính hay chi phí phát sinh từ việc sử
                dụng hoặc tin cậy vào công cụ. Công cụ được cung cấp với mục tiêu hỗ trợ và cảnh báo
                sớm cho người dùng nhưng chúng tôi không cam kết đảm bảo mọi nguy cơ đều được phát
                hiện.
              </p>
              <p className="text-justify">
                <i>Sự hạn chế của công nghệ: </i>Công cụ của chúng tôi áp dụng các kỹ thuật tiên
                tiến, nhưng công nghệ không thể hoàn hảo và có thể xảy ra các cảnh báo không chính
                xác hoặc bỏ sót. Chúng tôi không chịu trách nhiệm nếu các cảnh báo này không hoàn
                toàn chính xác trong mọi tình huống.
              </p>
            </div>
            <div className="py-10">
              <h2 className="text-xl font-medium mb-2">Sửa đổi điều khoản</h2>
              <p className="text-justify">
                <i>Cập nhật điều khoản: </i>Chúng tôi cam kết cải thiện liên tục và có thể thay đổi
                điều khoản dịch vụ này để phù hợp với các thay đổi trong công nghệ và phản hồi từ
                người dùng. Điều khoản cập nhật sẽ được thông báo trên trang web và có hiệu lực ngay
                khi công bố mà không thông báo cụ thể cho người dùng. Người dùng cần kiểm tra thường
                xuyên để đảm bảo hiểu rõ các điều khoản mới nhất.
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default TermsPage;
