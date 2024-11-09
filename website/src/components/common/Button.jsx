import PropTypes from 'prop-types';

function Button({ title, type = 'button', isDisable = false, handleClick }) {
  return (
    <button
      className={`inline-block px-4 py-2 rounded-lg transition-transform duration-200 ease-in-out
        ${
          isDisable
            ? 'bg-gray-300 text-gray-700 cursor-default'
            : 'bg-secondary text-white hover:scale-105 sm:hover:scale-100 hover:shadow-lg'
        }
      `}
      type={type}
      disabled={isDisable}
      {...(handleClick && !isDisable && { onClick: handleClick })}
    >
      {title}
    </button>
  );
}

Button.propTypes = {
  title: PropTypes.string.isRequired,
  type: PropTypes.string,
  handleClick: PropTypes.func,
  isDisable: PropTypes.bool,
};

export default Button;
