import ProTypes from 'prop-types';

function Loader({ fullScreen = false }) {
  let className = 'flex justify-center items-center';
  if (fullScreen) {
    className += ' fixed top-0 left-0 w-screen h-screen z-[999] bg-tertiary';
  } else {
    className += ' w-full h-full';
  }

  return (
    <div className={className}>
      <div className="loader relative w-12 h-12 rounded-full border-t-4 border-t-primary border-r-4 border-r-transparent animate-spin">
        <div className="absolute inset-0 w-12 h-12 rounded-full border-b-4 border-b-secondary border-l-4 border-l-transparent"></div>
      </div>
    </div>
  );
}

Loader.propTypes = {
  fullScreen: ProTypes.bool,
};

export default Loader;
