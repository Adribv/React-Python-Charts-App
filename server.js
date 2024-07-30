const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcrypt');
const admin = require('firebase-admin');

const app = express();
const PORT = 5000;

// Initialize Firebase Admin SDK
const serviceAccount = require('./config/serviceAccountKey.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://nissan-58a39-default-rtdb.firebaseio.com/' // Replace with your database URL
});

const db = admin.firestore();

app.use(cors());
app.use(bodyParser.json());

// Sign-up endpoint
app.post('/signup', async (req, res) => {
  const { username, email, password } = req.body;
  try {
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    
    // Save user data to Firestore
    await db.collection('users').doc(email).set({
      username,
      email,
      password: hashedPassword
    });

    res.status(201).json({ message: 'User signed up successfully!' });
  } catch (error) {
    console.error('Error signing up user:', error);
    res.status(500).json({ message: 'Failed to sign up user!' });
  }
});

// Sign-in endpoint
app.post('/signin', async (req, res) => {
  const { email, password } = req.body;
  try {
    const userSnapshot = await db.collection('users').doc(email).get();
    if (!userSnapshot.exists) {
      return res.status(404).json({ message: 'User not found!' });
    }
    const user = userSnapshot.data();
    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
      return res.status(401).json({ message: 'Invalid credentials!' });
    }
    res.status(200).json({ message: 'User signed in successfully!', user });
  } catch (error) {
    console.error('Error signing in user:', error);
    res.status(500).json({ message: 'Failed to sign in!' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
