import React from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
const Layout = ({ children, isHome=true }) => {
  return (
    <div>
      {isHome && <Navbar />}
      <main>{children}</main>
      {isHome && <Footer />}
    </div>
  );
};

export default Layout;
