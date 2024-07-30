import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/signin', { email, password });
      // Redirect to homepage on successful sign-in
      navigate('/dash', { replace: true });
    } catch (error) {
      setErrorMessage('Failed to sign in. Please check your credentials and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const pageStyle = {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundImage: 'url(https://i.ibb.co/5RHTzxx/Screenshot-2024-06-25-185451.png)',
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  };

  const signInContainerStyle = {
    width: '400px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '5px',
    backgroundColor: 'rgba(255, 255, 255, 0.5)', // Half-transparent white background
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  };

  const inputFieldStyle = {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '5px'
  };

  const signInButtonStyle = {
    display: 'block',
    width: '100%',
    padding: '10px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px',
    opacity: isLoading ? 0.7 : 1,
    pointerEvents: isLoading ? 'none' : 'auto'
  };

  const signUpTextStyle = {
    textAlign: 'center',
    marginTop: '10px'
  };

  const signUpLinkStyle = {
    color: '#28a745',
    textDecoration: 'none',
    cursor: 'pointer'
  };

  const handleSignUpClick = (event) => {
    event.preventDefault();
    navigate('/signup');
  };

  return (
    <div style={pageStyle}>
      <div style={signInContainerStyle}>
        <h2>Sign In</h2>
        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
        <form onSubmit={handleSignIn}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={inputFieldStyle}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputFieldStyle}
          />
          <button type="submit" style={signInButtonStyle} disabled={isLoading}>
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>
        <p style={signUpTextStyle}>
          New user? <a href="/signup" style={signUpLinkStyle} onClick={handleSignUpClick}>Sign Up Here</a>
        </p>
      </div>
    </div>
  );
};

export default SignIn;
