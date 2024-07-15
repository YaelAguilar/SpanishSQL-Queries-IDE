import PropTypes from 'prop-types';

const Footer = ({ tokens, className }) => {
  return (
    <footer className={`bg-[#13002B] p-4 ${className} flex flex-col min-h-40`}>
      <div className="flex space-x-4">
        <button className="text-lg">Problemas</button>
        <button className="text-lg">Terminal</button>
      </div>
      <div className="mt-4 border-t border-gray-700 pt-4 overflow-y-auto flex-grow">
        <p className="font-bold">Consola</p>
        <pre className="text-sm">
          {tokens.map((token, index) => (
            <div key={index}>
              <strong>{token.type}:</strong> {token.value}
            </div>
          ))}
        </pre>
      </div>
    </footer>
  );
};

Footer.propTypes = {
  tokens: PropTypes.array.isRequired,
  className: PropTypes.string,
};

export default Footer;
