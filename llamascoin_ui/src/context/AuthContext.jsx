import React, { createContext, useContext, useState, useMemo } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authData, setAuthData] = useState(() => {
    const storedData = localStorage.getItem('authData');
    return storedData ? JSON.parse(storedData) : { 
      accessToken: null,
      refreshToken: null,
      username: null,
      role: null,
      userId: null,
    };
  });

  const login = async (data) => {
    setAuthData((prevAuthData) => {
      const newAuthData = {
        ...prevAuthData,
        accessToken: data.access,
        refreshToken: data.refresh,
        username: data.username,
        role: data.role,
        userId: data.user_id,
      };
      localStorage.setItem('authData', JSON.stringify(newAuthData));
      return newAuthData;
    });
  };

  const logout = () => {
    setAuthData({ 
      accessToken: null,
      refreshToken: null,
      username: null,
      role: null,
      userId: null,
    });
    localStorage.removeItem('authData'); 
  };

  const value = useMemo(() => ({ authData, login, logout }), [authData]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
