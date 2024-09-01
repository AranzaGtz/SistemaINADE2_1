import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import * as TYPE from '../types/authTypes';

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  organization: string;
}

interface AuthState {
  access: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  user: User | null;
  message: string;
  error: any;
}

const initialState: AuthState = {
  access: localStorage.getItem('access'),
  isAuthenticated: false,
  loading: true,
  user: null,
  message: "",
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginSuccess: (state, action: PayloadAction<any>) => {
      localStorage.setItem('access', action.payload.access);
      state.access = action.payload.access;
      state.isAuthenticated = true;
      state.loading = false;
      state.user = action.payload.user;
      state.message = "Login has succeeded";
      state.error = null;
    },
    loginFail: (state, action: PayloadAction<any>) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
      state.message = "Login has failed";
      state.error = action.payload;
    },
    authenticatedSuccess: (state) => {
      state.isAuthenticated = true;
      state.loading = false;
    },
    authenticatedFail: (state) => {
      state.isAuthenticated = false;
      state.loading = false;
    },
    userLoadedSuccess: (state, action: PayloadAction<any>) => {
      state.user = action.payload;
      state.loading = false;
    },
    userLoadedFail: (state) => {
      state.user = null;
      state.loading = false;
    },
    refreshSuccess: (state, action: PayloadAction<any>) => {
      localStorage.setItem('access', action.payload.access);
      state.access = action.payload.access;
      state.isAuthenticated = true;
      state.loading = false;
      state.message = "Refresh token success";
    },
    refreshFail: (state) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
      state.message = "Refresh token failed";
    },
    logout: (state) => {
      localStorage.removeItem('access');
      state.access = null;
      state.isAuthenticated = false;
      state.loading = false;
      state.user = null;
      state.message = "User has logged out";
    },
    guestView: (state) => {
      state.user = null;
      state.loading = false;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    changePasswordSuccess: (state) => {
      state.message = "Change password success";
    },
    changePasswordFail: (state) => {
      state.message = "Change password failed";
    },
    signupSuccess: (state) => {
      state.message = "Verification link has been sent to your email";
    },
    signupFail: (state) => {
      state.message = "Signup failed";
    },
    activateAccountSuccess: (state) => {
      state.message = "Your account has been verified";
    },
    activateAccountFail: (state) => {
      state.message = "Account verification failed";
    },
    resetSuccess: (state) => {
      state.message = "Password reset success";
    },
    resetFail: (state) => {
      state.message = "Password reset failed";
    },
    setSuccess: (state) => {
      state.message = "Your new password has been set";
    },
    setFail: (state) => {
      state.message = "Setting new password failed";
    },
  },
});

export const {
  loginSuccess,
  loginFail,
  authenticatedSuccess,
  authenticatedFail,
  userLoadedSuccess,
  userLoadedFail,
  refreshSuccess,
  refreshFail,
  logout,
  guestView,
  setLoading,
  changePasswordSuccess,
  changePasswordFail,
  signupSuccess,
  signupFail,
  activateAccountSuccess,
  activateAccountFail,
  resetSuccess,
  resetFail,
  setSuccess,
  setFail,
} = authSlice.actions;

export default authSlice.reducer;
