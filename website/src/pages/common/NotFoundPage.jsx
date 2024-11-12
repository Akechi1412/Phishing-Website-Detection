import { Button } from '../../components/common';
import { EmptyLayout } from '../../components/layout';
import { Helmet, HelmetProvider } from 'react-helmet-async';

function NotFoundPage() {
  return (
    <HelmetProvider>
      <EmptyLayout>
        <Helmet>
          <title>404 - Không tìm thấy trang</title>
        </Helmet>
        <div className="h-screen flex flex-col justify-center">
          <div className="container px-5 sm:px-4">
            <div className="text-center px-6 py-4">
              <h1 className="text-9xl font-bold mb-4 text-secondary">404</h1>
              <p className="text-2xl mb-6 text-primary">
                Xin lỗi, trang bạn tìm kiếm không tồn tại.
              </p>
              <a href="/">
                <Button title="Quay về trang chủ" />
              </a>
            </div>
          </div>
        </div>
      </EmptyLayout>
    </HelmetProvider>
  );
}

export default NotFoundPage;
