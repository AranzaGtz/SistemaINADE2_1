import React, { useState, ChangeEvent, FormEvent } from "react";
import { Link, Navigate } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { signup } from "@/store/actions/authActions";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AppDispatch } from "@/store/store";
import axios from "axios";

const mapStateToProps = (state: any) => ({
  isAuthenticated: state.auth.isAuthenticated,
});

const mapDispatchToProps = (dispatch: AppDispatch) => ({
  signup: (
    first_name: string,
    last_name: string,
    email: string,
    password: string,
    re_password: string
  ) => dispatch(signup(first_name, last_name, email, password, re_password)),
});

// Usar ConnectedProps para obtener los tipos de las props
const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

// Combine all props types
type Props = PropsFromRedux;

const Signup: React.FC<Props> = ({ signup, isAuthenticated }) => {
  const [accountCreated, setAccountCreated] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    re_password: "",
  });

  const { first_name, last_name, email, password, re_password } = formData;

  const onChange = (e: ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (password === re_password) {
      signup(email, first_name, last_name, password, re_password);
      setAccountCreated(true);
    }
  };

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
    return <Navigate to="/" />;
  }
  if (accountCreated) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="container mt-5">
      <h1>Sign Up</h1>
      <p>Create your Account</p>
      <Card>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <Label htmlFor="first_name">First Name*</Label>
            <Input
              type="text"
              placeholder="First Name*"
              name="first_name"
              value={first_name}
              onChange={onChange}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="last_name">Last Name*</Label>
            <Input
              type="text"
              placeholder="Last Name*"
              name="last_name"
              value={last_name}
              onChange={onChange}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="email">Email*</Label>
            <Input
              type="email"
              placeholder="Email*"
              name="email"
              value={email}
              onChange={onChange}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="password">Password*</Label>
            <Input
              type="password"
              placeholder="Password*"
              name="password"
              value={password}
              onChange={onChange}
              minLength={6}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="re_password">Confirm Password*</Label>
            <Input
              type="password"
              placeholder="Confirm Password*"
              name="re_password"
              value={re_password}
              onChange={onChange}
              minLength={6}
              required
            />
          </div>
          <Button className="btn btn-primary" type="submit">
            Register
          </Button>
        </form>
        <Button className="btn btn-danger mt-3" onClick={continueWithGoogle}>
          Continue With Google
        </Button>
        <p className="mt-3">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </Card>
    </div>
  );
};

export default connector(Signup);
