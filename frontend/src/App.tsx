// src/App.tsx
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./layout/Layout";
import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";
import TestPage from "./pages/TestPage";

import Login from "./modules/auth/components/Login";
import Signup from "./modules/auth/components/Signup";
import Activate from "./modules/auth/components/Activate";
import Google from "./modules/auth/components/Google";
import ResetPassword from "./modules/auth/components/ResetPassword";
import ResetPasswordConfirm from "./modules/auth/components/ResetPasswordConfirm";

import DashboardPage from "./pages/DashboardPage";
import Laboratories from "./modules/lab/components/Laboratories";
import "./styles/App.css";
import PrivateRoute from "./routes/PrivateRoute";

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="" element={<HomePage />} />
          <Route
            path="dashboard"
            element={
              <PrivateRoute>
                <DashboardPage />{" "}
              </PrivateRoute>
            }
          />
          <Route path="login/" element={<Login />}></Route>
          <Route path="signup/" element={<Signup />}></Route>
          <Route path="google/" element={<Google />}></Route>
          <Route path="reset-password/" element={<ResetPassword />}></Route>
          <Route path="activate/:uid/:token" element={<Activate />}></Route>
          <Route
            path="/password/reset/confirm/:uid/:token"
            element={<ResetPasswordConfirm />}
          ></Route>
          <Route path="laboratories" element={<Laboratories />} />
          <Route path="test" element={<TestPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
