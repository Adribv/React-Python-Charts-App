import React from 'react';
import './HomePage.css'; // Import your CSS file
import logo from './logo.png'; // Replace with your actual logo file path

const HomePage = () => {

  const containerStyle = {
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif',
    padding: '100px', // Reduced padding to move the container up
    maxWidth: '600px',
    margin: 'auto',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    borderRadius: '5px',
    opacity: 0.5,
    marginTop: '0px'
  };

  const selectStyle = {
    padding: '12px',  // Adjusted padding for better alignment
    fontSize: '1rem',
    width: '100%',
    maxWidth: '300px',
    borderRadius: '5px',
    border: '1px solid #dddddd',
    backgroundColor: '#f9f9f9',
    color: '#333333',
    cursor: 'pointer',
    outline: 'none'
  };

  const selectContainerStyle = {
    marginTop: '20px'
  };

  // Function to handle page navigation
  const handleNavigation = (event) => {
    const selectedPage = event.target.value;
    if (selectedPage !== '') {
      window.location.href = selectedPage;
    }
  };

  const handleLogout = () => {
    window.location.href = '/logout';
  };

  return (
    <div className="container">
      <button 
        onClick={handleLogout}
        style={{
          position: 'absolute',
          top: '60px',  // Consistent top position for the button
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
        onMouseLeave={(e) => e.target.style.backgroundColor = '#f44336'}  // Original red when not hovered
      >
        Logout
      </button>
      <div className="sidebar">
        <div className="logo">
          <img src={logo} alt="Logo" />
        </div>
        <ul>
          {/* Add sidebar menu items if needed */}
        </ul>
      </div>

      <div className="navbar">
        <ul>
          {/* Add navbar menu items if needed */}
        </ul>
      </div>

      <div className="contente">
        <div style={containerStyle}>
          <div style={selectContainerStyle}>
            <select style={selectStyle} onChange={handleNavigation}>
              <option value="">Select Page</option>
              <option value="/dash">Sentiment on Features</option>
              <option value="/dash2">Graph On Features</option>
              <option value="/dash3">Sentiment Analysis</option>
              <option value="/dash4">Feedback</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
