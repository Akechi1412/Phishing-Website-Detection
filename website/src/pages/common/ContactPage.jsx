import { useState } from 'react';
import { Button, Input, Loader, TextArea } from '../../components/common';
import { MainLayout } from '../../components/layout';
import Swal from 'sweetalert2';
import { contactApi } from '../../apis';
import ReCAPTCHA from 'react-google-recaptcha';

function ContactPage() {
  const siteKey = import.meta.env.PD_CAPCHA_SITE_KEY;
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [content, setContent] = useState('');
  const [fullNameError, setFullNameError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [contentError, setContentError] = useState('');
  const [loading, setLoading] = useState(false);
  const [captchaVerified, setCaptchaVerified] = useState(false);
  const [captchaExpired, setCaptchaExpired] = useState(false);

  const handleFullNameChange = (event) => {
    setFullName(event.target.value);
    const fullName = event.target.value.trim();
    const alphaRegex =
      /^[a-zA-Z_ÀÁÂÃÈÉÊẾÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêếìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ ]+$/;
    if (fullName === '') {
      setFullNameError('Họ và tên bắt buộc!');
      return;
    }
    if (fullName.length < 2 || fullName.length > 50) {
      setFullNameError('Họ và tên phải có độ dài từ 2 đến 50 ký tự!');
      return;
    }
    if (!alphaRegex.test(fullName)) {
      setFullNameError('Họ và tên không được chứa số hoặc ký tự đặc biệt!');
      return;
    }
    setFullNameError('');
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
    const email = event.target.value.trim();
    const emailRegex =
      /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    if (email === '') {
      setEmailError('Email là bắt buộc!');
      return;
    }
    if (!emailRegex.test(email)) {
      setEmailError('Email không hợp lệ!');
      return;
    }
    setEmailError('');
  };

  const handleContentChange = (event) => {
    setContent(event.target.value);
    const content = event.target.value.trim();
    if (content === '') {
      setContentError('Nội dung là bắt buộc!');
      return;
    }
    if (content.length > 10000) {
      setContent('Nội dung có tối đa 10000 ký tự');
      return;
    }
    setContentError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await contactApi.send({ user_name: fullName, user_email: email, message: content });
      setLoading(false);
      await Swal.fire({
        icon: 'success',
        title: 'Gửi liên hệ thành công',
        text: 'Cảm ơn bạn đã gửi liên hệ cho chúng tôi',
        timer: 2000,
      });
    } catch (error) {
      setLoading(false);
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Có lỗi gì đó xảy ra, vui lòng thử lại!',
      });
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

  return (
    <MainLayout>
      <div className="py-8 sm:py-6">
        <div className="container mx-auto px-5 sm:px-4">
          <h1 className="text-3xl sm:text-2xl text-primary font-bold mb-6 animate-appear-from-left">
            Liên hệ
          </h1>
          <p className="mb-6">
            Liên hệ trực tiếp qua email{' '}
            <a
              className="text-secondary hover:underline transition-all"
              href="mailto:info@phishdetect.net"
            >
              info@phishdetect.net
            </a>{' '}
            hoặc điền vào biểu mẫu dưới đây. Chúng tôi sẽ phản hồi trong thời gian sớm nhất có thể.
          </p>
          <div className="flex justify-center">
            <form
              className="p-6 rounded-lg w-[700px] max-w-full shadow-[0_0_40px_-15px_rgba(0,0,0,0.3)] space-y-4 min-h-[300px]"
              action=""
              onSubmit={handleSubmit}
            >
              {!loading ? (
                <>
                  {' '}
                  <div className="flex flex-col">
                    <label className="mb-2" htmlFor="fullName">
                      Họ và tên <span className="text-red-700">*</span>
                    </label>
                    <Input
                      value={fullName}
                      id="fullName"
                      name="fullName"
                      placeholder="Ví dụ: Nguyễn Văn A"
                      handleChange={handleFullNameChange}
                    />
                    {fullNameError && <p className="mt-2 text-red-500">{fullNameError}</p>}
                  </div>
                  <div className="flex flex-col">
                    <label className="mb-2" htmlFor="email">
                      Email <span className="text-red-700">*</span>
                    </label>
                    <Input
                      value={email}
                      type="email"
                      id="email"
                      name="email"
                      placeholder="Ví dụ: nguyenvana@gmail.com"
                      handleChange={handleEmailChange}
                    />
                    {emailError && <p className="mt-2 text-red-500">{emailError}</p>}
                  </div>
                  <div className="flex flex-col">
                    <label className="mb-2" htmlFor="content">
                      Nội dung <span className="text-red-700">*</span>
                    </label>
                    <TextArea
                      value={content}
                      name="content"
                      id="content"
                      rows={4}
                      placeholder="Nội dung cần liên hệ"
                      handleChange={handleContentChange}
                    />
                    {contentError && <p className="mt-2 text-red-500">{contentError}</p>}
                  </div>
                  <div className="flex justify-center mb-5">
                    <ReCAPTCHA
                      sitekey={siteKey}
                      onChange={handleCaptchaChange}
                      onExpired={handleCaptchaExpired}
                    />
                  </div>
                  <div className="flex justify-end">
                    <Button
                      type="submit"
                      title="Xác nhận"
                      isDisable={
                        !fullName ||
                        !email ||
                        !content ||
                        fullNameError ||
                        emailError ||
                        contentError ||
                        !captchaVerified ||
                        captchaExpired
                      }
                    />
                  </div>
                </>
              ) : (
                <Loader />
              )}
            </form>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

export default ContactPage;
