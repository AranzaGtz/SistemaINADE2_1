import React from "react";
import { useSelector } from "react-redux";
import { RootState } from "@/store/store";
import { AdminNavbar, CustomerNavbar, GuestNavbar } from "./Navbar";
import { AdminSidebar, CustomerSidebar, GuestSidebar } from "./Sidebar";
import Footer from "./Footer";
import { Outlet } from "react-router-dom";

const Layout: React.FC = () => {
  const { isAuthenticated, user } = useSelector(
    (state: RootState) => state.auth
  );

  const renderNavbar = () => {
    if (!isAuthenticated) {
      return <GuestNavbar />;
    }
    switch (user?.role) {
      case "Admin":
        return <AdminNavbar />;
      case "Customer":
        return <CustomerNavbar />;
      default:
        return <GuestNavbar />;
    }
  };

  const renderSidebar = () => {
    if (!isAuthenticated) {
      return <GuestSidebar />;
    }
    switch (user?.role) {
      case "Admin":
        return <AdminSidebar />;
      case "Customer":
        return <CustomerSidebar />;
      default:
        return <GuestSidebar />;
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      {renderNavbar()}
      <div className="flex flex-grow">
        {renderSidebar()}
        <main className="flex-grow p-4">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
