import React from 'react';

import './CheckWeather.css';

const CheckWeather = ({ dateDict, setDateDict, isFavorite, prediction, onSubmitForm, onClickChangeFavorite }) => {
  const [city, setCity] = React.useState('');
  

  return (
    <div style={{ margin: '0' }} className='center-form col-5 offset-1'>
      <h1>Погода в вашем городе</h1>
      <form onSubmit={(e) => onSubmitForm(e, city, dateDict)} method='post'>
        <label htmlFor='city'>Город:</label>
        <input
          value={city}
          onChange={(e) => setCity(e.target.value)}
          type='text'
          name='city'
          className='form-control'
          id='city'
          placeholder='Введите город'
          maxLength='30'
          required
        />

        <div className='form-floating' style={{ width: '50%' }}>
          <input
            type='date'
            id='date'
            name='date'
            value={dateDict.current}
            min={dateDict.min}
            max={dateDict.max}
            onChange={(e) =>
              setDateDict({ current: e.target.value, min: dateDict.min, max: dateDict.max })
            }
          />
        </div>

        <input type='submit' name='send' value='Узнать' className='mt-2 btn btn-warning' />
      </form>

      {Object.keys(prediction).length !== 0 && (
        <>
          <h2 style={{ marginTop: '20px', width: '600px' }}>
            Информация о погоде {prediction.date}
          </h2>
          <div className='alert alert-warning'>
            <div className='row'>
              <div className='col-9'>
                <b>Город:</b> {prediction.city.name}
                <br />
                <b>Температура:</b> {prediction.temp}
                <sup>o</sup>
                <br />
                <b>Осадки:</b> {prediction.precipitation}
                <br />
                <b>Вероятность осадков:</b> {prediction.precipitation_probability}%
                <br />
                <b>Вероятность осадков от ИИ:</b> {prediction.precipitation_probability_ai}%
              </div>
              <div className='col-2 offset-1'>
                <img src={prediction.icon} alt='Фото погоды' className='img-thumbnail' />
              </div>
              <button
                onClick={() => onClickChangeFavorite(prediction.city.name)}
                id='favorite-button'
                className='favorite_button'
                type='submit'>
                <i
                  className={(isFavorite ? 'fa-solid' : 'fa-regular') + ' fa-star'}
                  style={{ color: 'orange' }}></i>
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default CheckWeather;
