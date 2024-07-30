@echo off

rem Commands to run Python scripts
start python dash_app4.py
start python dash_app3.py
start python dash_app2.py
start python dash_app.py

rem Commands to run Node.js server
start node server.js

rem Wait for a moment to let previous commands start
timeout /t 10 /nobreak > nul

rem Commands to install npm packages
call npm install

rem Commands to start the app
call npm start
