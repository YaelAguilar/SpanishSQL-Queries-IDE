import { useState } from 'react';
import PropTypes from 'prop-types';

const Sidebar = ({ onFileOpen }) => {
  const [files, setFiles] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newFileName, setNewFileName] = useState('');

  const handleAddFile = (e) => {
    e.preventDefault();
    if (newFileName) {
      setFiles([...files, newFileName]);
      setNewFileName('');
      setShowForm(false);
      onFileOpen(newFileName);
    }
  };

  const handleDeleteFile = (fileName) => {
    if (window.confirm(`Are you sure you want to delete ${fileName}?`)) {
      setFiles(files.filter(file => file !== fileName));
    }
  };

  return (
    <aside className="w-64 bg-[#0F0021] p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg">Project</h2>
        <button 
          title="Add New" 
          className="text-lg"
          onClick={() => setShowForm(!showForm)}
        >
          +
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleAddFile} className="mb-4">
          <input
            type="text"
            value={newFileName}
            onChange={(e) => setNewFileName(e.target.value)}
            placeholder="Enter file name"
            className="w-full p-2 mb-2 bg-gray-700 text-white"
          />
          <button type="submit" className="w-full p-2 bg-[#13002B] text-white">
            Add File
          </button>
        </form>
      )}
      <ul className="space-y-2">
        {files.map((file, index) => (
          <li 
            key={index} 
            className="flex justify-between items-center cursor-pointer p-2 transition-all duration-400 hover:text-red-500 hover:bg-gray-700 hover:shadow-md hover:rounded-md"
            onClick={() => onFileOpen(file)}
          >
            <span>{file}</span>
            <button 
              className="text-red-500 ml-2" 
              onClick={(e) => {
                e.stopPropagation();
                handleDeleteFile(file);
              }}
            >
              x
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
};

Sidebar.propTypes = {
  onFileOpen: PropTypes.func.isRequired,
};

export default Sidebar;
