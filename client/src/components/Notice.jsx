import React from 'react';

const Notice = ({ isError, message }) => {
  if (!message) {
    return;
  }

  return (
    <>
      {isError ? (
        <div className='alert alert-danger' role='alert'>
          {message}
        </div>
      ) : (
        <div className='alert alert-success' role='alert'>
          {message}
        </div>
      )}
    </>
  );
};

export default Notice;
