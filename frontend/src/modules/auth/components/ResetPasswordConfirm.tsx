import React, { useState, ChangeEvent, FormEvent } from "react";
import { Navigate, useParams } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { resetPasswordConfirm } from "@/store/actions/authActions";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const mapDispatchToProps = {
  resetPasswordConfirm,
};

const connector = connect(null, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

const ResetPasswordConfirm: React.FC<Props> = ({ resetPasswordConfirm }) => {
  const [requestSent, setRequestSent] = useState(false);
  const [formData, setFormData] = useState({
    new_password: "",
    re_new_password: "",
  });

  const { new_password, re_new_password } = formData;
  const { uid, token } = useParams<{ uid: string; token: string }>();

  const onChange = (e: ChangeEvent<HTMLInputElement>) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (uid && token) {
      resetPasswordConfirm(uid, token, new_password, re_new_password);
      setRequestSent(true);
    }
  };

  if (requestSent) {
    return <Navigate to="/" />;
  }

  return (
    <div className="container mt-5">
      <h1>Reset Your Password</h1>
      <Card>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <Label htmlFor="new_password">New Password</Label>
            <Input
              type="password"
              placeholder="New Password"
              name="new_password"
              value={new_password}
              onChange={onChange}
              minLength={6}
              required
            />
          </div>
          <div className="form-group">
            <Label htmlFor="re_new_password">Confirm New Password</Label>
            <Input
              type="password"
              placeholder="Confirm New Password"
              name="re_new_password"
              value={re_new_password}
              onChange={onChange}
              minLength={6}
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

export default connector(ResetPasswordConfirm);
