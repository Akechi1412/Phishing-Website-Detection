import PropTypes from 'prop-types';

function EmptyLayout({ children, className }) {
  return <div className={className}>{children}</div>;
}

EmptyLayout.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
};

export default EmptyLayout;
