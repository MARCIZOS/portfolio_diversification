import React, { createContext, useState, useEffect } from 'react';
import { getCurrentUser, loginUser, signupUser } from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error("Auth initialization failed:", error);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (username, password) => {
    const data = await loginUser(username, password);
    localStorage.setItem('token', data.access_token);
    setUser({ username: data.username });
  };

  const signup = async (username, email, password) => {
    const data = await signupUser(username, email, password);
    localStorage.setItem('token', data.access_token);
    setUser({ username: data.username });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
