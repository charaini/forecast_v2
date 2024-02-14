import React from 'react';
import { Navigate, useParams } from 'react-router-dom';

import axios from '../axios';
import { useSelector } from 'react-redux';
import { selectIsAuth } from '../redux/slices/auth';

const CityHistory = () => {
  const isAuth = useSelector(selectIsAuth);
  const { cityId } = useParams();
  const [predictions, setPredictions] = React.useState([]);
  const [cityName, setCityName] = React.useState('Неизвестно');

  React.useEffect(() => {
    axios
      .get(`/weather/prediction/?city_id=${cityId}`)
      .then((res) => setPredictions(res.data.predictions))
      .catch((err) => console.log(`Error: ${err}`));
    axios
      .get(`/weather/city/?city_id=${cityId}`)
      .then((res) => setCityName(res.data.name))
      .catch((err) => console.log(`Error: ${err}`));
  }, []);

  if (!isAuth) {
    return <Navigate to='/login' />;
  }

  return (
    <div className='profile-form' style={{ margin: '100px auto 0', minHeight: '400px' }}>
      <h2 style={{ textAlign: 'center', fontSize: '35px' }}>Город: {cityName}</h2>
      {predictions.length !== 0 ? (
        <>
          {predictions.map((pred) => (
            <div key={pred.id} className='alert alert-warning'>
              <div className='row'>
                <div className='col-9'>
                  <b>Город:</b> {pred.city_id.name}
                  <br />
                  <b>Дата:</b> {pred.date}
                  <br />
                  <b>Осадки:</b> {pred.precipitation_type.name}
                  <br />
                  <b>Вероятность осадков:</b> {pred.precipitation_probability}%
                  <br />
                  <b>Вероятность осадков от ИИ:</b> {pred.precipitation_probability_ai}%
                </div>
              </div>
            </div>
          ))}
        </>
      ) : (
        <h4 style={{ textAlign: 'center', marginTop: '50px' }}>История запросов отсутствует</h4>
      )}
    </div>
  );
};

export default CityHistory;
