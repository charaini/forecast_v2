import React from 'react';
import { Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import { fetchAuth, selectIsAuth } from '../redux/slices/auth';

const Login = () => {
  const isAuth = useSelector(selectIsAuth);
  const dispatch = useDispatch();

  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [isError, setError] = React.useState(false);

  const onSubmitForm = async (e) => {
    e.preventDefault();

    const formdata = new FormData();
    formdata.append('username', username);
    formdata.append('password', password);

    const data = await dispatch(fetchAuth(formdata));
    if (data.payload) {
      window.localStorage.setItem('token', data.payload.access);
      window.location.href = '/'
    } else {
      setError(true);
    }
  };

  if (isAuth) {
    return <Navigate to='/' />;
  }

  return (
    <div className='center-container'>
      <form onSubmit={onSubmitForm} className='center-form' method='POST'>
        <h1 style={{ marginLeft: '220px', marginBottom: '70px' }}> Вход </h1>

        <div className='form-group'>
          <label htmlFor='login'>Введите логин</label>
          <input
            type='text'
            name='login'
            className='form-control'
            id='login'
            aria-describedby='usernameHelp'
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='password'>Введите пароль</label>
          <input
            type='password'
            name='password'
            className='form-control'
            id='password'
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {isError && (
          <p style={{ margin: '30px 0 0 0', color: 'red' }}>Неправильный логин или пароль</p>
        )}

        <button type='submit' className='btn btn-outline-warning'>
          Войти
        </button>
      </form>
    </div>
  );
};

export default Login;
