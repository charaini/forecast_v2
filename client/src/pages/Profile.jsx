import React from 'react';
import { Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import { selectIsAuth, selectUsername, fetchAuthMe } from '../redux/slices/auth';
import History from '../components/History';
import axios from '../axios';

const Profile = () => {
  const dispatch = useDispatch();
  const isAuth = useSelector(selectIsAuth);

  const name = useSelector(selectUsername);
  const [username, setUsername] = React.useState(name);
  const [password, setPassword] = React.useState('');

  const [isError, setError] = React.useState(false);
  const [errorText, setErrorText] = React.useState('');

  const onSubmitUserForm = (e) => {
    e.preventDefault();
    setError(false);
    setErrorText('');

    const formdata = new FormData();
    if (username) formdata.append('username', username);
    if (password) formdata.append('password', password);

    axios
      .put('/user/me/', formdata)
      .then(async (res) => {
        await dispatch(fetchAuthMe());
        alert('Данные успешно обновлены');
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

  if (!isAuth) {
    return <Navigate to='/login' />;
  }

  return (
    <>
      <div className='profile-form' style={{ margin: '100px auto 0', minHeight: '600px' }}>
        <h2 style={{ textAlign: 'center', fontSize: '35px' }}>Кабинет пользователя</h2>

        <div>
          <form onSubmit={onSubmitUserForm} method='POST'>
            <div className='form-group'>
              <label htmlFor='login'>Логин пользователя:</label>
              <input
                type='text'
                name='login'
                className='form-control'
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                id='login'
                aria-describedby='usernameHelp'
              />
            </div>
            <div className='form-group'>
              <label htmlFor='password'>Введите пароль:</label>
              <input
                type='password'
                onChange={(e) => setPassword(e.target.value)}
                name='password'
                className='form-control'
                id='password'
                value={password}
              />
            </div>
            {isError && <p className='form__error'>{errorText}</p>}
            <button className='button form__button' type='submit'>
              Обновить данные
            </button>
          </form>
          <History />
        </div>
      </div>
    </>
  );
};

export default Profile;
