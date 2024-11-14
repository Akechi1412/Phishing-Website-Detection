import { forwardRef } from 'react';
import PropTypes from 'prop-types';

const Input = forwardRef(({ type = 'text', placeholder, value, handleChange, id, name }, ref) => {
  return (
    <input
      type={type}
      className="outline-none border border-tertiary px-2 py-1 rounded focus:border-secondary transition-all"
      placeholder={placeholder}
      value={value}
      onChange={handleChange}
      id={id}
      name={name}
      ref={ref}
    />
  );
});

Input.displayName = 'Input';

Input.propTypes = {
  type: PropTypes.string,
  placeholder: PropTypes.string,
  value: PropTypes.any,
  handleChange: PropTypes.func,
  id: PropTypes.string,
  name: PropTypes.string,
};

export default Input;
