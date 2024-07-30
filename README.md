# Project: Dashboard Web Application with Authentication firebase and react and python

## Overview

This project implements a web application with features for user authentication, dashboard display using React and Dash, and a Node.js backend server for API integration. It provides a seamless user experience for signing up, signing in, navigating through different dashboard views, and logging out.

## Features

- *Authentication*: Users can sign up with a username, email, and password securely stored using bcrypt encryption. Sign-in functionality verifies credentials against stored data.
  
- *Dashboard Integration*: The application includes multiple dashboard views powered by Dash applications embedded within React components.
  
- *Navigation*: Navigation between different dashboard views and the homepage is facilitated through a dropdown menu.
  
- *Logout*: Users can securely log out of their sessions to protect their account information.

## Setup Instructions

### Prerequisites

- Install Python (version X.X.X) and Node.js (version X.X.X) on your system.
- Ensure npm (Node Package Manager) is installed for managing dependencies.

### Installation

### Note this does not contain the serviceAccountKey.json of firebaase So Keep Your SecretKey You Generate From Firebase In The Config Folder Also Change The Server.js Firebase DB Link 

1. *Clone the Repository*

   ```bash
   git clone https://github.com/your/repository.git
   cd repository-name

Running Server Or app
----------------------

Double Click On the run_app.bat To Run The Application And Wait For 30 Sec For The Deployment To Start 


OR If The run_app.bat Is Not Working Then Follow The Below Steps
----------------------------------------------------------------



Running Node.js Server
----------------------

bash

Copy code

node server.js

Dash Applications
-----------------

bash

Copy code

`python dash_app.py
python dash_app2.py
python dash_app3.py
python dash_app4.py`

Frontend Setup
--------------

bash

Copy code

npm install

Running React Application
-------------------------

bash

Copy code

npm start

Usage
-----

-   Navigate to http://localhost:3000 in your web browser to access the application.
-   Sign up or sign in using the provided forms.
-   Explore different dashboard views using the navigation dropdown.
-   Log out securely after usage.

Technologies Used
-----------------

-   *Frontend*: React.js, Axios, React Router
-   *Backend*: Node.js, Express.js, bcrypt
-   *Database*: Firebase (Realtime Database or Firestore)
-   *Visualization*: Dash (Python framework for creating analytical web applications)

Troubleshooting
---------------

If encountering issues during setup or usage, ensure all dependencies are correctly installed and configured as per the instructions.

Contributors
------------

-   List of contributors or credits if applicable.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
