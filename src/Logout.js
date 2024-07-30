import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear any authentication tokens or user data stored in local storage or cookies
    localStorage.removeItem('authToken'); // or your token key
    // Redirect to sign-in page
    navigate('/signin', { replace: true });
  }, [navigate]);

  return null;
};

export default Logout;
