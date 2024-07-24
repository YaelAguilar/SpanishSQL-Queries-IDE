import PropTypes from 'prop-types';

const Console = ({ logs = [], className }) => {
  return (
    <footer className={`bg-[#13002B] p-4 ${className} flex flex-col min-h-40`}>
      <div className="flex space-x-4">
        <button className="text-lg">Problemas</button>
        <button className="text-lg">Terminal</button>
      </div>
      <div className="mt-4 border-t border-gray-700 pt-4 overflow-y-auto flex-grow">
        <p className="font-bold">Consola</p>
        <pre className="text-sm">
          {logs.length > 0 ? logs.map((log, index) => (
            <div key={index}>
              {log}
            </div>
          )) : "No logs available"}
        </pre>
      </div>
    </footer>
  );
};

Console.propTypes = {
  logs: PropTypes.array,
  className: PropTypes.string,
};

export default Console;
