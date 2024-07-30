import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import DashApp from './components/DashApp';
import DashApp2 from './components/DashApp2';
import DashApp3 from './components/DashApp3';
import DashApp4 from './components/DashApp4';
import HomePage from './HomePage';

import Logout from './Logout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/signin" />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/dash" element={<DashApp />} />
        <Route path="/dash2" element={<DashApp2 />} />
        <Route path="/dash3" element={<DashApp3 />} />
        <Route path="/dash4" element={<DashApp4 />} />
        <Route path="/homepage" element={<HomePage />} />
    
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
}

export default App;
