import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

const ConnectDBPage = ({ onDbConnect }) => {
  const [formData, setFormData] = useState({
    user: '',
    password: '',
    host: '',
    port: '',
    database: ''
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleDbConnect = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/connect_db', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        onDbConnect(formData);
        navigate('/ide');
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error('Error connecting to the database:', error);
      alert('Error connecting to the database');
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-900">
      <form className="bg-gray-800 p-6 rounded shadow-md text-white" onSubmit={handleDbConnect}>
        <h2 className="text-lg font-semibold mb-4">Connect to Database</h2>
        <div className="mb-4">
          <label className="block mb-2">User</label>
          <input
            type="text"
            name="user"
            value={formData.user}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Host</label>
          <input
            type="text"
            name="host"
            value={formData.host}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Port</label>
          <input
            type="text"
            name="port"
            value={formData.port}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Database (Optional)</label>
          <input
            type="text"
            name="database"
            value={formData.database}
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700"
          />
        </div>
        <button type="submit" className="w-full p-2 bg-blue-500 rounded hover:bg-blue-700">Connect</button>
      </form>
    </div>
  );
};

ConnectDBPage.propTypes = {
  onDbConnect: PropTypes.func.isRequired,
};

export default ConnectDBPage;
