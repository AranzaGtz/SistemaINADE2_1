import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import * as TYPE from '../types/authTypes';

interface AuthState {
  access: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  user: any;
}

const initialState: AuthState = {
  access: localStorage.getItem('access'),
  isAuthenticated: false,
  loading: true,
  user: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    [TYPE.LOGIN_SUCCESS]: (state, action: PayloadAction<any>) => {
      localStorage.setItem('access', action.payload.access);
      state.access = action.payload.access;
      state.isAuthenticated = true;
      state.loading = false;
      state.user = action.payload.user;
    },
    [TYPE.LOGIN_FAIL]: (state) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
    },
    [TYPE.AUTHENTICATED_SUCCESS]: (state) => {
      state.isAuthenticated = true;
      state.loading = false;
    },
    [TYPE.AUTHENTICATED_FAIL]: (state) => {
      state.isAuthenticated = false;
      state.loading = false;
    },
    [TYPE.USER_LOADED_SUCCESS]: (state, action: PayloadAction<any>) => {
      state.user = action.payload;
      state.loading = false;
    },
    [TYPE.USER_LOADED_FAIL]: (state) => {
      state.user = null;
      state.loading = false;
    },
    [TYPE.REFRESH_SUCCESS]: (state, action: PayloadAction<any>) => {
      localStorage.setItem('access', action.payload.access);
      state.access = action.payload.access;
      state.isAuthenticated = true;
      state.loading = false;
      state.user = action.payload.user;
    },
    [TYPE.REFRESH_FAIL]: (state) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
    },
    [TYPE.LOGOUT]: (state) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
    },
    [TYPE.GUEST_VIEW]: (state) => {
      state.user = null;
      state.loading = false;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { actions } = authSlice;
export default authSlice.reducer;
