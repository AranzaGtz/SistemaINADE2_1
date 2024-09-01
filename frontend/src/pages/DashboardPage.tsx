import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "@/store/store";
import { getUser } from "@/store/actions/authActions";
import { Button, Spinner } from "@/components/index";

const DashboardPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user, loading } = useSelector((state: RootState) => state.auth);

  useEffect(() => {
    if (!user) {
      dispatch(getUser());
    }
  }, [dispatch, user]);

  if (loading) {
    return <Spinner />;
  }

  if (!user) {
    return <Spinner />;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-4xl font-bold text-center">
        Hola Mundo desde DashboardPage
      </h1>
      <div className="mt-4">
        <p>
          <strong>ID:</strong> {user.id}
        </p>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <p>
          <strong>First Name:</strong> {user.first_name}
        </p>
        <p>
          <strong>Last Name:</strong> {user.last_name}
        </p>
        <p>
          <strong>Role:</strong> {user.role}
        </p>
        <p>
          <strong>Organization:</strong> {user.organization}
        </p>
      </div>
      <Button>Hello</Button>
    </div>
  );
};

export default DashboardPage;
