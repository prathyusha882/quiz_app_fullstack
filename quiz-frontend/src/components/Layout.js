import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Header from './common/Header';
import Footer from './common/Footer';
import './Layout.css';

const Layout = ({ children }) => {
  const { user } = useAuth();

  return (
    <div className="layout">
      <Header user={user} />
      <main className="layout-main">
        <div className="container">
          {children}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;