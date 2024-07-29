import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import IDEPage from "./pages/IDEPage";
import ConnectDBPage from './pages/ConnectDBPage';
import Error404Page from './pages/Error404Page';

function App() {
  const [dbCredentials, setDbCredentials] = useState(null);

  const handleDbConnect = (credentials) => {
    setDbCredentials(credentials);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ConnectDBPage onDbConnect={handleDbConnect} />} />
        <Route path="/ide" element={dbCredentials ? <IDEPage dbCredentials={dbCredentials} /> : <Navigate to="/" />} />
        <Route path="*" element={<Error404Page />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
