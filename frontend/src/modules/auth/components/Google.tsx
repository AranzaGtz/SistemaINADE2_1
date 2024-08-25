import React, { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { connect, ConnectedProps } from "react-redux";
import { googleAuthenticate } from "@/store/actions/authActions";
import queryString from "query-string";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const mapDispatchToProps = {
  googleAuthenticate,
};

const connector = connect(null, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

const Google: React.FC<Props> = ({ googleAuthenticate }) => {
  let location = useLocation();

  useEffect(() => {
    const values = queryString.parse(location.search);
    const state = values.state as string | null;
    const code = values.code as string | null;

    if (state && code) {
      googleAuthenticate(state, code);
    }
  }, [location, googleAuthenticate]);

  return (
    <div className="container">
      <Card className="mt-5">
        <h1 className="display-4">Welcome to Auth System!</h1>
        <p className="lead">
          This is an incredible authentication system with production level
          features!
        </p>
        <hr className="my-4" />
        <p>Click the Log In button</p>
        <Link to="/login">
          <Button className="btn btn-primary btn-lg" role="button">
            Login
          </Button>
        </Link>
      </Card>
    </div>
  );
};

export default connector(Google);
