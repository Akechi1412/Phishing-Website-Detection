import Logo from '../../assets/phish_detect.svg';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="h-20 sm:h-16 bg-tertiary sticky top-0 left-0 shadow-lg shadow-gray-300/50">
      <div className="container h-full px-5 sm:px-4">
        <div className="h-full flex justify-between items-center">
          <Link
            to="/"
            className="flex flex-col justify-center items-center animate-appear-from-left"
          >
            <img height={80} width={80} src={Logo} alt="PhishDetect" className="w-16 sm:w-12" />
            <div className="font-bold text-sm sm:text-xs">
              <span className="text-primary">PhishDetect</span>
              <span className="text-secondary">.net</span>
            </div>
          </Link>
          <nav className="h-full animate-appear-from-right">
            <ul className="h-full flex items-center space-x-5">
              <li>
                <Link
                  className="relative pb-1 hover:text-secondary after:block after:absolute after:left-0 after:right-0 after:bottom-0 after:h-[2px] after:bg-secondary after:scale-x-0 hover:after:scale-x-100 after:origin-right hover:after:origin-left after:transition-transform after:duration-300"
                  to="/"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  className="relative pb-1 hover:text-secondary after:block after:absolute after:left-0 after:right-0 after:bottom-0 after:h-[2px] after:bg-secondary after:scale-x-0 hover:after:scale-x-100 after:origin-right hover:after:origin-left after:transition-transform after:duration-300"
                  to="/extension"
                >
                  Extension
                </Link>
              </li>
              <li>
                <a
                  className="relative pb-1 hover:text-secondary after:block after:absolute after:left-0 after:right-0 after:bottom-0 after:h-[2px] after:bg-secondary after:scale-x-0 hover:after:scale-x-100 after:origin-right hover:after:origin-left after:transition-transform after:duration-300"
                  href="https://github.com/Akechi1412/Phishing-Website-Detection"
                >
                  Resource
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
