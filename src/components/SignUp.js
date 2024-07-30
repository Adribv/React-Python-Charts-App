import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/signup', { username, email, password });
      alert(response.data.message);
      navigate('/signin', { replace: true });
    } catch (error) {
      setErrorMessage('Failed to sign up. Please check your details and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const styles = {
    container: {
      width: '400px',
      margin: '0 auto',
      padding: '20px',
      border: '1px solid #ccc',
      borderRadius: '5px',
      backgroundColor: 'rgba(255, 255, 255, 0.5)',
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
    },
    inputField: {
      width: '100%',
      padding: '10px',
      marginBottom: '10px',
      fontSize: '16px',
      border: '1px solid #ccc',
      borderRadius: '5px',
    },
    button: {
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
    },
    linkText: {
      textAlign: 'center',
      marginTop: '10px',
    },
    link: {
      color: '#28a745',
      textDecoration: 'none',
    },
    body: {
      backgroundImage: "url('https://i.ibb.co/5RHTzxx/Screenshot-2024-06-25-185451.png')",
      backgroundSize: 'cover',
      backgroundRepeat: 'no-repeat',
      backgroundAttachment: 'fixed',
      height: '100vh',
      margin: 0,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    },
    errorMessage: {
      color: 'red',
      marginBottom: '10px',
    },
  };

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h2>Sign Up</h2>
        {errorMessage && <p style={styles.errorMessage}>{errorMessage}</p>}
        <form onSubmit={handleSignUp}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={styles.inputField}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.inputField}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.inputField}
          />
          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Signing Up...' : 'Sign Up'}
          </button>
        </form>
        <p style={styles.linkText}>
          Already registered?{' '}
          <Link to="/signin" style={styles.link}>
            Sign In Here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;
