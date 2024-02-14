import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

import { selectIsAuth } from '../redux/slices/auth';
import Notice from '../components/Notice';
import CheckWeather from '../components/CheckWeather/CheckWeather';
import CitiesList from '../components/CitiesList';
import axios from '../axios';

const Index = () => {
  const isAuth = useSelector(selectIsAuth);

  const [isLoading, setLoading] = React.useState(true);
  const [isError, setError] = React.useState(false);
  const [noticeMessage, setNoticeMessage] = React.useState('');
  const [citiesInfo, setCitiesInfo] = React.useState([]);
  const [dateDict, setDateDict] = React.useState({ current: '', min: '', max: '' });
  const [prediction, setPrediction] = React.useState({});
  const [isFavorite, setFavorite] = React.useState(false);

  const setFetchError = () => {
    setError(true);
    setNoticeMessage('Произошла ошибка при получении данных о погоде');
  };

  const fetchWeather = (updateDates = true) => {
    axios
      .get('/weather/')
      .then((res) => {
        const data = res.data;
        if (updateDates) {
          setDateDict(data.dates);
        }
        setCitiesInfo(data.cities);

        if (data.error_message) {
          setError(true);
          setNoticeMessage(data.error_message);
        }
      })
      .catch(() => {
        setFetchError();
      })
      .finally(() => setLoading(false));
  };

  React.useEffect(() => {
    if (isAuth) {
      fetchWeather();
    }
  }, []);

  const onSubmitWeatherForm = (e, city, dateDict) => {
    e.preventDefault();

    const formdata = new FormData();
    formdata.append('city', city);
    formdata.append('date', dateDict.current);

    axios
      .post('/weather/', formdata)
      .then((res) => {
        setPrediction(res.data.prediction);
        setFavorite(res.data.prediction.city.is_favorite);
        fetchWeather(false);
      })
      .catch(() => {
        setFetchError();
      });
  };

  const onClickChangeFavorite = (city) => {
    setError(false);
    axios
      .post('/weather/city/', { city })
      .then((res) => {
        if (isFavorite) {
          setError(true);
        }

        setFavorite(!isFavorite);
        setNoticeMessage(res.data.message);
      })
      .catch(() => {
        setError(true);
        setNoticeMessage('Произошла ошибка');
      });
  };

  if (!isAuth) {
    return <Navigate to='/login' />;
  }

  return (
    <div className='container mt-5'>
      <div className='row'>
        <Notice isError={isError} message={noticeMessage} />

        <CheckWeather
          dateDict={dateDict}
          setDateDict={setDateDict}
          prediction={prediction}
          isFavorite={isFavorite}
          onSubmitForm={onSubmitWeatherForm}
          onClickChangeFavorite={onClickChangeFavorite}
        />

        <CitiesList isLoading={isLoading} cities={citiesInfo} />
      </div>
    </div>
  );
};

export default Index;
