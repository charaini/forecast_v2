import React from 'react';
import { Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import axios from '../axios';
import { authUser, selectIsAuth } from '../redux/slices/auth';

const Registration = () => {
  const isAuth = useSelector(selectIsAuth)

  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmPass, setConfirmPass] = React.useState('');
  const [isError, setError] = React.useState(false);
  const [errorText, setErrorText] = React.useState('');

  const dispatch = useDispatch();

  const onSubmitForm = async (e) => {
    e.preventDefault();
    setError(false);
    setErrorText('');

    if (password !== confirmPass) {
      setError(true);
      setErrorText('Пароли не совпадают');
      return;
    }

    const formdata = new FormData();
    formdata.append('username', username);
    formdata.append('password', password);

    axios
      .post('/user/register/', formdata)
      .then((res) => {
        const userData = { username: res.data.user.username, isAdmin: res.data.user.is_staff };
        dispatch(authUser(userData));
        window.localStorage.setItem('token', res.data.token);
      })
      .catch((err) => {
        setError(true);
        setErrorText('Произошла ошибка. Попробуйте еще раз.');

        const usernameError = err.response?.data?.username;
        const passwordError = err.response?.data?.password;

        if (usernameError) {
          setErrorText(usernameError);
        } else if (passwordError) {
          setErrorText(passwordError);
        }
      });
  };

  if (isAuth) {
    return <Navigate to='/' />;
  }

  return (
    <div className='center-container'>
      <form onSubmit={onSubmitForm} className='center-form' method='POST'>
        <h1 style={{ marginLeft: '220px', marginBottom: '70px' }}> Регистрация </h1>

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
          <label htmlFor='password1'>Введите пароль</label>
          <input
            type='password'
            name='password1'
            className='form-control'
            id='password1'
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className='form-group'>
          <label htmlFor='password2'>Введите пароль еще раз</label>
          <input
            type='password'
            name='password2'
            className='form-control'
            id='password2'
            value={confirmPass}
            onChange={(e) => setConfirmPass(e.target.value)}
            required
          />
        </div>

        {isError && <p style={{ margin: '30px 0 0 0', color: 'red' }}>{errorText}</p>}

        <button type='submit' className='btn btn-outline-warning'>
          Зарегистрироваться
        </button>
      </form>
    </div>
  );
};

export default Registration;
