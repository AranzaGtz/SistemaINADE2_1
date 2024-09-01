import React, { useState, ChangeEvent, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { login } from "@/store/actions/authActions";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { RootState } from "@/store/store";

const mapStateToProps = (state: RootState) => ({
  isAuthenticated: state.auth.isAuthenticated,
});

const mapDispatchToProps = {
  login,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

const Login: React.FC<Props> = ({ login, isAuthenticated }) => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const { email, password } = formData;

  const navigate = useNavigate();

  const onChange = (e: ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    login(email, password);
  };

  const goSignup = () => navigate("/signup");

  const goForgotPassword = () => navigate("/forgot-password");

  const continueWithGoogle = async () => {
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/auth/o/google-oauth2/?redirect_uri=${process.env.REACT_APP_API_URL}/google`
      );
      window.location.replace(res.data.authorization_url);
    } catch (err) {
      console.error(err);
    }
  };

  if (isAuthenticated) {
    navigate("/");
  }

  return (
    <div className="container mt-5">
      <h1>Sign In</h1>
      <p>Sign into your Account</p>
      <Card>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <Label htmlFor="email">Email</Label>
            <Input
              type="email"
              placeholder="Email"
              name="email"
              value={email}
              onChange={onChange}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="password">Password</Label>
            <Input
              type="password"
              placeholder="Password"
              name="password"
              value={password}
              onChange={onChange}
              minLength={6}
              required
            />
          </div>
          <Button className="btn btn-primary" type="submit">
            Login
          </Button>
        </form>
        <Button className="btn btn-danger mt-3" onClick={continueWithGoogle}>
          Continue With Google
        </Button>
        <br />
        <p className="mt-3" onClick={goSignup}>
          Don't have an account? Sign Up
        </p>
        <p className="mt-3" onClick={goForgotPassword}>
          Forgot your Password? Reset Password
        </p>
      </Card>
    </div>
  );
};

export default connector(Login);
