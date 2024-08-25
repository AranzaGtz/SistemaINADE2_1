import React, { useState } from "react";
import { Navigate, useParams } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { verify } from "@/store/actions/authActions";
import { Button } from "@/components/ui/button";
import { AppDispatch } from "@/store/store";

const mapDispatchToProps = (dispatch: AppDispatch) => ({
  verify: (uid: string, token: string) => dispatch(verify(uid, token)),
});

const connector = connect(null, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

const Activate: React.FC<Props> = ({ verify }) => {
  const [verified, setVerified] = useState(false);
  const { uid, token } = useParams<{ uid: string; token: string }>();

  const verifyAccount = () => {
    if (uid && token) {
      verify(uid, token);
      setVerified(true);
    }
  };

  if (verified) {
    return <Navigate to="/" />;
  }

  return (
    <div className="container">
      <div
        className="d-flex flex-column justify-content-center align-items-center"
        style={{ marginTop: "200px" }}
      >
        <h1>Verify your Account:</h1>
        <Button
          onClick={verifyAccount}
          style={{ marginTop: "50px" }}
          type="button"
          className="btn btn-primary"
        >
          Verify
        </Button>
      </div>
    </div>
  );
};

export default connector(Activate);
