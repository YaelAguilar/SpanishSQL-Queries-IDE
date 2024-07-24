import { BrowserRouter, Routes, Route } from 'react-router-dom';
//import { UserProvider } from './Components/context/UserContext';  
import IDEPage from "./pages/IDEPage";
import Error404Page from './pages/Error404Page';

function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<IDEPage />} />
          <Route path="*" element={<Error404Page />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;