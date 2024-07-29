import IDEContainer from "../containers/IDEContainer";
import PropTypes from 'prop-types';

const IDEPage = ({ dbCredentials }) => {
  return (
    <IDEContainer dbCredentials={dbCredentials} />
  );
}

IDEPage.propTypes = {
  dbCredentials: PropTypes.object.isRequired,
};

export default IDEPage;
