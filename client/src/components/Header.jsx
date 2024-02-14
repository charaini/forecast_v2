import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import { selectIsAuth, selectIsAdmin, logout } from '../redux/slices/auth';

const Header = () => {
  const dispatch = useDispatch();
  const isAdmin = useSelector(selectIsAdmin);
  const isAuth = useSelector(selectIsAuth);

  const onClickLogout = () => {
    if (window.confirm('Вы уверены, что хотите выйти из аккаунта?')) {
      dispatch(logout());
      window.localStorage.removeItem('token');
      window.location.href = '/';
    }
  };

  return (
    <header>
      <div className='container d-flex justify-content-between align-items-center'>
        <Link
          to='/'
          className='d-flex align-items-center text-decoration-none'
          style={{ padding: '20px' }}>
          <span className='fs-3'>Прогноз погоды</span>
        </Link>
        <nav className='d-none d-md-flex' style={{ marginRight: '-300px' }}>
          {isAdmin && (
            <Link to='/graph' className='me-3 link-body-emphasis text-decoration-none fs-5'>
              График
            </Link>
          )}
          <Link to='/' className='me-3 link-body-emphasis text-decoration-none fs-5'>
            Главная
          </Link>
          <a className='me-3 link-body-emphasis text-decoration-none fs-5' href='#info'>
            Информация
          </a>
          <a className='me-3 link-body-emphasis text-decoration-none fs-5' href='#support'>
            Поддержка
          </a>
          <a className='me-3 link-body-emphasis text-decoration-none fs-5' href='#prices'>
            Цены
          </a>
        </nav>
        <div className='d-flex' style={{ marginRight: '-70px' }}>
          {isAuth ? (
            <>
              <Link to='/profile'>
                <button type='button' className='button me-3 py-2 w-30 fs-5'>
                  Профиль
                </button>
              </Link>
              <button onClick={onClickLogout} type='button' className='button me-3 py-2 w-30 fs-5'>
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to='/registration'>
                <button type='button' className='button me-3 py-2 w-30 fs-5'>
                  Регистрация
                </button>
              </Link>
              <Link to='/login'>
                <button type='button' className='button py-2 fs-5'>
                  Вход
                </button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
