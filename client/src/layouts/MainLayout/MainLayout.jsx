import React from 'react';
import { Outlet } from 'react-router-dom';

import Header from '../../components/Header';

import './users.css';
import './weather.css';

const MainLayout = () => {
  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
    </>
  );
}

export default MainLayout;
