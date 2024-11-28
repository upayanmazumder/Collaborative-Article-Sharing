"use client"

import React, { useState } from 'react';
import axios from 'axios';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('https://api.cas.upayan.dev/auth/signup', {
        email,
        password,
      });

      setMessage(`Signup successful! User ID: ${response.data.uid}`);
      setError(''); // Clear any previous errors
      setEmail('');
      setPassword('');
    } catch (err) {
      setMessage('');
      setError(err.response?.data?.error || 'An error occurred during signup.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', textAlign: 'center' }}>
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
        <div style={{ marginBottom: '15px' }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              padding: '10px',
              width: '100%',
              borderRadius: '5px',
              border: '1px solid #ccc',
            }}
            required
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              padding: '10px',
              width: '100%',
              borderRadius: '5px',
              border: '1px solid #ccc',
            }}
            required
          />
        </div>
        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Signup
        </button>
      </form>
      {message && (
        <div style={{ marginTop: '20px', color: 'green' }}>
          <strong>{message}</strong>
        </div>
      )}
      {error && (
        <div style={{ marginTop: '20px', color: 'red' }}>
          <strong>{error}</strong>
        </div>
      )}
    </div>
  );
};

export default Signup;
