import React from 'react';

import './NotFound.css';

const NotFound = () => {
  return (
    <div className='error-form center-form'>
      <h1 className='error-title'>Страница не найдена</h1>
      <h3 className='error-code'>404</h3>
    </div>
  );
};

export default NotFound;
