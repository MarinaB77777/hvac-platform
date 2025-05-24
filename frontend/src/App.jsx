import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import LoginPage from "./pages/LoginPage"
import OrdersList from "./pages/OrdersList"
import MyOrders from "./pages/MyOrders"
import ClientLogin from "./pages/ClientLogin"
import ClientOrders from "./pages/ClientOrders"
import WarehouseLogin from "./pages/WarehouseLogin"
import WarehouseRequests from "./pages/WarehouseRequests"
import WarehouseMovement from "./pages/WarehouseMovement"
import ManagerLogin from "./pages/ManagerLogin"
import ManagerAnalytics from "./pages/ManagerAnalytics"
import ManagerHvac from "./pages/ManagerHvac"
import { getUserRole, isAuthenticated } from "./auth/auth"

export default function App() {
  const role = getUserRole()

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        {/* Сохранившиеся старые маршруты */}
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

        {/* Новое — автонавигация по роли */}
        <Route
          path="/"
          element={
            isAuthenticated()
              ? <Navigate to={`/${role}`} />
              : <Navigate to="/login" />
          }
        />
      </Routes>
    </BrowserRouter>
  )
}
