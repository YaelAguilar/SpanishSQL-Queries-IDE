import PropTypes from 'prop-types';

const WelcomeScreen = ({ textColor, backgroundColor }) => {
  return (
    <div className="flex-1 flex flex-col justify-center items-center p-4" style={{ backgroundColor: backgroundColor }}>
      <h1 className="text-4xl mb-4" style={{ color: textColor }}>Welcome to CustomCode IDE</h1>
      <p className="text-lg" style={{ color: textColor }}>
        CustomCode IDE is a powerful code editor designed to help you write, debug, and manage your code efficiently.
        Create or open a file to get started.
      </p>
    </div>
  );
};

WelcomeScreen.propTypes = {
  textColor: PropTypes.string,
  backgroundColor: PropTypes.string,
};

export default WelcomeScreen;
