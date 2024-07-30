// src/api.js

export const fetchChartData = async () => {
    try {
      const response = await fetch('/api/chart-data'); // Adjust this URL to match your API endpoint
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Fetch error:', error);
      return []; // Return an empty array or handle the error appropriately
    }
  };
  