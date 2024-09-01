import React from "react";
import { useNavigate } from "react-router-dom";

export const AdminSidebar: React.FC = () => {
  const navigate = useNavigate();
  return (
    <nav>
      <ul>
        <li onClick={() => navigate("/")}>Dashboard</li>
        <li onClick={() => navigate("/settings")}>Settings</li>
        <li onClick={() => navigate("/logout")}>Logout</li>
      </ul>
    </nav>
  );
};

export const CustomerSidebar: React.FC = () => {
  const navigate = useNavigate();
  return (
    <nav>
      <ul>
        <li onClick={() => navigate("/")}>Dashboard</li>
        <li onClick={() => navigate("/settings")}>Settings</li>
        <li onClick={() => navigate("/logout")}>Logout</li>
      </ul>
    </nav>
  );
};

export const GuestSidebar: React.FC = () => {
  const navigate = useNavigate();
  return (
    <nav>
      <ul>
        <li onClick={() => navigate("/login")}>Login</li>
        <li onClick={() => navigate("/signup")}>Signup</li>
      </ul>
    </nav>
  );
};
