import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="border-t border-t-tertiary py-4">
      <div className="container px-5 sm:px-4">
        <ul className="w-full flex justify-center items-center space-x-4 sm:space-x-0 sm:space-y-1 sm:flex-col text-primary">
          <li>&copy; PhishDetect.net</li>
          <li>
            <Link className="text-secondary hover:underline" to="/terms">
              Điều khoản
            </Link>
          </li>
          <li>
            <Link className="text-secondary hover:underline" to="/policy">
              Chính sách
            </Link>
          </li>
          <li>
            <Link className="text-secondary hover:underline" to="/">
              Liên hệ
            </Link>
          </li>
        </ul>
      </div>
    </footer>
  );
}

export default Footer;
