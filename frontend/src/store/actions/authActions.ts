import axios from "axios";
import { AppDispatch } from "../store";
import * as TYPE from "../types/authTypes";
import { API_BASE_URL } from "@/constants/urls";
axios.defaults.withCredentials = true;

export const loadUser = () => async (dispatch: AppDispatch) => {
  if (localStorage.getItem('access')) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem('access')}`,
      },
    };

    try {
      const res = await axios.get(`${API_BASE_URL}/auth/users/me/`, config);
      dispatch({
        type: TYPE.USER_LOADED_SUCCESS,
        payload: res.data,
      });
    } catch (err) {
      dispatch({
        type: TYPE.USER_LOADED_FAIL,
      });
    }
  } else {
    dispatch({
      type: TYPE.USER_LOADED_FAIL,
    });
  }
};

export const googleAuthenticate = (state: string, code: string) => async (dispatch: AppDispatch) => {
  if (state && code && !localStorage.getItem('access')) {
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    };

    const details = {
      'state': state,
      'code': code
    };

    const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

    try {
      const res = await axios.post(`${API_BASE_URL}/auth/o/google-oauth2/?${formBody}`, config);

      dispatch({
        type: TYPE.GOOGLE_AUTH_SUCCESS,
        payload: res.data
      });

      dispatch(loadUser());
    } catch (err) {
      dispatch({
        type: TYPE.GOOGLE_AUTH_FAIL
      });
    }
  }
};

export const checkAuthenticated = () => async (dispatch: AppDispatch) => {
  if (localStorage.getItem('access')) {
    const config = {
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    };
    const body = JSON.stringify({ token: localStorage.getItem('access') });

    try {
      const res = await axios.post(`${API_BASE_URL}/auth/jwt/verify/`, body, config);

      if (res.data.code !== 'token_not_valid') {
        dispatch({
          type: TYPE.AUTHENTICATED_SUCCESS,
        });
      } else {
        dispatch({
          type: TYPE.AUTHENTICATED_FAIL,
        });
        dispatch(refreshToken());
      }
    } catch (err) {
      dispatch({
        type: TYPE.AUTHENTICATED_FAIL,
      });
    }
  } else {
    dispatch({
      type: TYPE.AUTHENTICATED_FAIL,
    });
  }
};

export const login = (email: string, password: string) => async (dispatch: AppDispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ email, password });

  try {
    const res = await axios.post(`${API_BASE_URL}/auth/jwt/create/`, body, config);
    dispatch({
      type: TYPE.LOGIN_SUCCESS,
      payload: res.data,
    });
  } catch (err) {
    dispatch({
      type: TYPE.LOGIN_FAIL,
    });
  }
};

export const signup = (email: string, first_name: string, last_name: string, password: string, re_password: string) => async (dispatch: AppDispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ email, first_name, last_name, password, re_password });
  
  try {
    await axios.post(`${API_BASE_URL}/auth/users/`, body, config);
    dispatch({
      type: TYPE.SIGNUP_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: TYPE.SIGNUP_FAIL,
    });
  }
};

export const verify = (uid: string, token: string) => async (dispatch: AppDispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ uid, token });

  try {
    await axios.post(`${API_BASE_URL}/auth/users/activation/`, body, config);
    dispatch({
      type: TYPE.ACTIVATE_ACCOUNT_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: TYPE.ACTIVATE_ACCOUNT_FAIL,
    });
  }
};

export const resetPassword = (email: string) => async (dispatch: AppDispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ email });

  try {
    await axios.post(`${API_BASE_URL}/auth/users/reset_password/`, body, config);
    dispatch({
      type: TYPE.PASSWORD_RESET_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: TYPE.PASSWORD_RESET_FAIL,
    });
  }
};

export const resetPasswordConfirm = (uid: string, token: string, new_password: string, re_new_password: string) => async (dispatch: AppDispatch) => {
  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  const body = JSON.stringify({ uid, token, new_password, re_new_password });

  try {
    await axios.post(`${API_BASE_URL}/auth/users/reset_password_confirm/`, body, config);
    dispatch({
      type: TYPE.PASSWORD_RESET_CONFIRM_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: TYPE.PASSWORD_RESET_CONFIRM_FAIL,
    });
  }
};

export const refreshToken = () => async (dispatch: AppDispatch) => {
  if (localStorage.getItem('refresh')) {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    const body = JSON.stringify({ refresh: localStorage.getItem('refresh') });

    try {
      const res = await axios.post(`${API_BASE_URL}/auth/jwt/refresh/`, body, config);
      dispatch({
        type: TYPE.REFRESH_SUCCESS,
        payload: res.data,
      });
    } catch (err) {
      dispatch({
        type: TYPE.REFRESH_FAIL,
      });
    }
  } else {
    dispatch({
      type: TYPE.REFRESH_FAIL,
    });
  }
};

export const logout = () => (dispatch: AppDispatch) => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  dispatch({
    type: TYPE.LOGOUT,
  });
};


export const changePassword = (current_password: string, new_password: string) => async (dispatch: AppDispatch) => {
  await dispatch(checkAuthenticated());

  const config = {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `JWT ${localStorage.getItem('access')}`,
    },
  };
  const body = JSON.stringify({ current_password, new_password });
  
  try {
    await axios.post(`${API_BASE_URL}/auth/users/set_password/`, body, config);
    dispatch({
      type: TYPE.CHANGE_PASSWORD_SUCCESS,
    });
  } catch (err) {
    dispatch({
      type: TYPE.CHANGE_PASSWORD_FAIL,
    });
  }
};