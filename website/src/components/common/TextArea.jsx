import PropTypes from 'prop-types';

function TextArea({ placeholder, value, id, name, handleChange, rows = 4 }) {
  return (
    <textarea
      id={id}
      name={name}
      value={value}
      placeholder={placeholder}
      onChange={handleChange}
      className="outline-none border border-tertiary p-2 rounded focus:border-secondary transition-all"
      rows={rows}
    ></textarea>
  );
}

TextArea.propTypes = {
  placeholder: PropTypes.string,
  value: PropTypes.string,
  handleChange: PropTypes.func,
  id: PropTypes.string,
  name: PropTypes.string,
  rows: PropTypes.number,
};

export default TextArea;
