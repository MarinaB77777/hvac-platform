import React from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

import LoginPage from "./pages/LoginPage"

import MyOrders from "./pages/hvac/MyOrders"
import MaterialsPage from "./pages/hvac/MaterialsPage"
import HVACLayout from "./pages/hvac/HVACLayout"
import MapOrders from "./pages/hvac/MapOrders"

import ClientLogin from "./pages/ClientLogin"
import ClientOrders from "./pages/client/ClientOrders"
import ClientLayout from "./pages/client/ClientLayout"
import ClientNewOrder from "./pages/client/ClientNewOrder"

import WarehouseLogin from "./pages/warehouse/WarehouseLogin"
import WarehouseRequests from "./pages/warehouse/WarehouseRequests"
import WarehouseMovement from "./pages/warehouse/WarehouseMovement"

import ManagerLogin from "./pages/manager/ManagerLogin"
import ManagerAnalytics from "./pages/manager/ManagerAnalytics"
import ManagerHvac from "./pages/manager/ManagerHvac"
import ManagerOrders from "./pages/manager/ManagerOrders"
import ManagerStock from "./pages/manager/ManagerStock"
import ManagerLayout from "./pages/manager/ManagerLayout"
import ManagerEfficiency from "./pages/manager/ManagerEfficiency"

import ManagerAi from "./pages/manager/ManagerAi"

import { getUserRole, isAuthenticated } from "./auth/auth"

export default function App() {
  const role = getUserRole()

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/client-login" element={<ClientLogin />} />
        <Route path="/warehouse-login" element={<WarehouseLogin />} />
        <Route path="/manager-login" element={<ManagerLogin />} />

        {/* HVAC */}
        {role === "hvac" && (
          <Route path="/hvac" element={<HVACLayout />}>
            <Route path="my-orders" element={<MyOrders />} />
            <Route path="materials" element={<MaterialsPage />} />
            <Route path="free-orders" element={<MapOrders />} />
          </Route>
        )}

        {/* Client */}
        {role === "client" && (
          <Route path="/client" element={<ClientLayout />}>
            <Route path="orders" element={<ClientOrders />} />
            <Route path="new" element={<ClientNewOrder />} />
            <Route path="profile" element={<div>Профиль (временно)</div>} />
          </Route>
        )}

        {/* Warehouse */}
        <Route path="/warehouse-requests" element={<WarehouseRequests />} />
        <Route path="/warehouse-movement" element={<WarehouseMovement />} />

       {role === "manager" && (
       <Route path="/manager" element={<ManagerLayout />}>
         <Route path="hvac" element={<ManagerHvac />} />
         <Route path="orders" element={<ManagerOrders />} />
         <Route path="stock" element={<ManagerStock />} />
         <Route path="efficiency" element={<ManagerEfficiency />} />
         <Route path="ai" element={<ManagerAi />} />
      </Route>
      )}
         
        {/* Автонавигация по роли */}
        <Route
          path="*"
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
