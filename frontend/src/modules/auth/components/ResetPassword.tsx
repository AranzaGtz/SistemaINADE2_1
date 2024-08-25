import React, { useState, ChangeEvent, FormEvent } from "react";
import { Navigate } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { resetPassword } from "@/store/actions/authActions";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const mapDispatchToProps = {
  resetPassword,
};

const connector = connect(null, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

const ResetPassword: React.FC<Props> = ({ resetPassword }) => {
  const [requestSent, setRequestSent] = useState(false);
  const [formData, setFormData] = useState({ email: "" });

  const { email } = formData;

  const onChange = (e: ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    resetPassword(email);
    setRequestSent(true);
  };

  if (requestSent) {
    return <Navigate to="/" />;
  }

  return (
    <div className="container mt-5">
      <h1>Request Password Reset:</h1>
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
          <Button className="btn btn-primary" type="submit">
            Reset Password
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default connector(ResetPassword);
