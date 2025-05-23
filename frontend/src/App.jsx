import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import OrdersList from "./pages/OrdersList";
import MyOrders from "./pages/MyOrders";
import ClientLogin from "./pages/ClientLogin";
import ClientOrders from "./pages/ClientOrders";
import WarehouseLogin from "./pages/WarehouseLogin";
import WarehouseRequests from "./pages/WarehouseRequests";
import WarehouseMovement from "./pages/WarehouseMovement";
import ManagerLogin from "./pages/ManagerLogin";
import ManagerAnalytics from "./pages/ManagerAnalytics";
import ManagerHvac from "./pages/ManagerHvac";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/orders" element={<OrdersList />} />
        <Route path="/my-orders" element={<MyOrders />} />
      <Route path="/client-login" element={<ClientLogin />} />
  <Route path="/client-orders" element={<ClientOrders />} />
  <Route path="/warehouse-login" element={<WarehouseLogin />} />
  <Route path="/warehouse-requests" element={<WarehouseRequests />} />
  <Route path="/warehouse-movement" element={<WarehouseMovement />} />
  <Route path="/manager-login" element={<ManagerLogin />} />
  <Route path="/manager-analytics" element={<ManagerAnalytics />} />
  <Route path="/manager-hvac" element={<ManagerHvac />} />
</Routes>
    </BrowserRouter>
  );
}
