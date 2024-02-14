import React from 'react';

const CitiesList = ({ isLoading, cities }) => {
  if (isLoading) {
    return (
      <div style={{ width: '470px', height: '100%' }} className='center-form col-4 offset-1'>
        <div style={{ textAlign: 'center' }}>
          Загрузка
        </div>
      </div>
    );
  }

  return (
    <div style={{ width: '470px', height: '100%' }} className='center-form col-4 offset-1'>
      <h2 style={{ fontSize: '30px' }}>Информация о погоде сейчас</h2>
      {cities.length !== 0 ? (
        cities.map((city, i) => (
          <div key={i} className='alert alert-warning'>
            <div className='row'>
              <div className='col-9'>
                <b>Город:</b> {city.city}
                <br />
                <b>Температура:</b> {city.temp}
                <sup>o</sup>
                <br />
                <b>Осадки:</b> {city.precipitation}
                <br />
                <b>Вероятность осадков:</b> {city.prob_precipitation}%
                <br />
              </div>
              <div className='col-2 offset-1'>
                <img src={city.icon} alt='Фото погоды' className='img-thumbnail' />
              </div>
            </div>
          </div>
        ))
      ) : (
        <p style={{ marginTop: '50px', textAlign: 'center' }}>Вы еще не делали запросов</p>
      )}
    </div>
  );
};

export default CitiesList;
