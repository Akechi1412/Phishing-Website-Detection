import PropTypes from 'prop-types';
import { Header, Footer } from '../common';

function MainLayout({ children, className }) {
  return (
    <div className={`min-h-screen flex flex-col ${className}`}>
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}

MainLayout.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
};

export default MainLayout;
