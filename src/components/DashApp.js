import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from './logo.png'; // Replace with your actual logo file path

function DashApp() {
  const navigate = useNavigate();

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    fontFamily: 'Arial, sans-serif',
    width: '100%',
    color: '#333333',
    backgroundColor: 'rgba(255, 255, 255, 0.6)', // Increased transparency
    marginTop: '20px',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  };

  const titleStyle = {
    fontSize: '2rem',
    marginBottom: '20px',
    color: '#333333',
  };

  const selectStyle = {
    padding: '12px',
    fontSize: '1rem',
    width: '100%',
    maxWidth: '300px',
    borderRadius: '5px',
    border: '1px solid #dddddd',
    backgroundColor: '#EBEBEB',
    color: '#333333',
    cursor: 'pointer',
    outline: 'none',
    transition: 'border-color 0.2s ease-in-out',
  };

  const logoStyle = {
    marginBottom: '20px',
    maxWidth: '100px', // Adjust the size of the logo here
  };

  const iframeContainerStyle = {
    width: '100%',
    marginTop: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  };

  const iframeStyle = {
    width: '100%',
    height: '80vh', // Height relative to viewport height for better visibility
    border: 'none',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
  };

  const handleNavigation = (event) => {
    const selectedPage = event.target.value;
    if (selectedPage !== '') {
      navigate(selectedPage);
    }
  };

  const handleLogout = () => {
    navigate('/logout');
  };

  return (
    <div className="content" style={{
      backgroundImage: 'url(https://i.ibb.co/Pxws1fY/Screenshot-2024-06-25-185451.png)',
      backgroundSize: 'cover',
      backgroundRepeat: 'no-repeat',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      padding: '20px',
      position: 'relative',  // Ensure that child elements are positioned relative to this container
    }}>
      <button 
        onClick={handleLogout}
        style={{
          position: 'absolute',
          top: '60px',  // Increased from 20px to 60px for more space from the top
          right: '20px',
          padding: '10px 20px',
          backgroundColor: '#f44336', // Red background for the logout button
          color: '#ffffff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
          fontSize: '1rem',
          fontWeight: 'bold',
          transition: 'background-color 0.3s ease',
        }}
        onMouseEnter={(e) => e.target.style.backgroundColor = '#c62828'}  // Darker red on hover
        onMouseLeave={(e) => e.target.style.backgroundColor = '#f44336'}  // Original red when not hoveredm
        
      >
        Logout
      </button>
      <div style={containerStyle}>
        <div style={logoStyle}>
          <img src={logo} alt="Logo" style={{ maxWidth: '100%', borderRadius: '5px' }} />
        </div>
        <h1 style={titleStyle}>Sentiment on Features</h1>
        <div>
          <select style={selectStyle} onChange={handleNavigation}>
            <option value="">Select Page</option>
            
            <option value="/dash2">Graph On Features</option> 
            <option value="/dash3">Sentiment Analysis</option>
            <option value="/dash4">Feedback</option>
           
          </select>
        </div>
        <div style={iframeContainerStyle}>
          <iframe title="dash-app" src="http://localhost:8057" style={iframeStyle}></iframe>
        </div>
      </div>
    </div>
  );
}

export default DashApp;
