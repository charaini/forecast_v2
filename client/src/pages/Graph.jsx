import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axios from '../axios';

import { API_DOMAIN } from '../App';
import { selectIsAuth, selectIsAdmin } from '../redux/slices/auth';

const Graph = () => {
  const isAuth = useSelector(selectIsAuth);
  const isAdmin = useSelector(selectIsAdmin);
  const [isLoading, setLoading] = React.useState(true);
  const [accuracy, setAccuracy] = React.useState(0);
  const [countPred, setCountPred] = React.useState(0);

  React.useEffect(() => {
    axios
      .get('/weather/graph/')
      .then((res) => {
        setAccuracy(res.data.accuracy);
        setCountPred(res.data.predictions_count);
        setLoading(false);
      })
      .catch((err) => console.log(`Error: ${err}`));
  }, []);

  if (!isAuth) {
    return <Navigate to='/login' />;
  }

  return (
    <div
      style={{ margin: '10px auto', width: '1000px', height: '100%' }}
      className='center-form graph-container'>
      {!isLoading ? (
        <>
          {isAdmin ? (
            <>
              <h2>Всего запросов за все время: {countPred}</h2>
              <h1 style={{ fontSize: '36px' }}>График вероятности осадков всех пользователей</h1>
            </>
          ) : (
            <h1>График вероятности осадков</h1>
          )}

          <h4>
            Точность нейронной сети: <b>{accuracy}</b>
          </h4>
          <div className='graph-blue'>Прогноз от сайта погоды</div>
          <div className='graph-orange'>Прогноз от нейронной сети</div>
          <img src={`${API_DOMAIN}/static/weather/img/plot.png`} alt='graph' />
          <a href={`${API_DOMAIN}/static/weather/graphs/graph.pdf`} download>
            <button className='button'>Выгрузить график</button>
          </a>
        </>
      ) : (
        <div>Загрузка</div>
      )}
    </div>
  );
};

export default Graph;
