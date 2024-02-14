import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from '../../axios';

export const fetchAuth = createAsyncThunk('auth/fetchAuth', async (params) => {
  const { data } = await axios.post('/token/', params);
  console.log('LOGIN data', data)
  return data;
});

export const fetchAuthMe = createAsyncThunk('auth/fetchAuthMe', async () => {
  const { data } = await axios.get('/user/me/');
  return data;
});

const initialState = {
  username: '',
  isAdmin: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    authUser: (state, action) => {
      state.username = action.payload.username;
      state.isAdmin = action.payload.isAdmin;
    },
    logout: (state) => {
      state.username = '';
    },
  },
  extraReducers: builder => {
    builder.addCase(fetchAuthMe.fulfilled, (state, action) => {
      state.username = action.payload.username;
      state.isAdmin = action.payload.is_staff;
    });
  }
});

export const selectUsername = (state) => state.auth.username;
export const selectIsAuth = (state) => Boolean(state.auth.username);
export const selectIsAdmin = (state) => Boolean(state.auth.isAdmin);

export const authReducer = authSlice.reducer;

export const { authUser, logout } = authSlice.actions;
