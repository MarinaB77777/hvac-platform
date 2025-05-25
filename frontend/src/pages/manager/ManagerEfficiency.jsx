> Муж:
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

        {/* Manager */}
        {role === "manager" && (
          <Route path="/manager" element={<ManagerLayout />}>
            <Route path="hvac" element={<ManagerHvac />} />
            <Route path="orders" element={<ManagerOrders />} />
            <Route path="stock" element={<ManagerStock />} />
            <Route path="efficiency" element={<ManagerAnalytics />} />
            <Route path="ai" element={<div>ИИ-анализ (временно)</div>} />
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

> Муж:
import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerEfficiency() {
  const [norms, setNorms] = useState([])
  const [newNorm, setNewNorm] = useState({ job: "", category: "", brand: "", max: 1 })

  useEffect(() => {
    loadNorms()
  }, [])

  const loadNorms = async () => {
    try {
      const res = await API.get("/material-norms")
      setNorms(res.data)
    } catch {
      alert("Ошибка загрузки норм")
    }
  }

  const updateNorm = async (id, field, value) => {
    try {
      await API.patch(`/material-norms/${id}`, { [field]: value })
      loadNorms()
    } catch {
      alert("Ошибка при обновлении")
    }
  }

  const deleteNorm = async (id) => {
    try {
      await API.delete(`/material-norms/${id}`)
      loadNorms()
    } catch {
      alert("Ошибка при удалении")
    }
  }

  const addNorm = async () => {
    try {
      await API.post("/material-norms", newNorm)
      setNewNorm({ job: "", category: "", brand: "", max: 1 })
      loadNorms()
    } catch {
      alert("Ошибка при добавлении")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Нормы расхода материалов</h1>

      <table className="w-full text-sm border mb-6">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-2 py-1">Тип работы</th>
            <th className="border px-2 py-1">Категория</th>
            <th className="border px-2 py-1">Марка</th>
            <th className="border px-2 py-1">Макс. (шт)</th>
            <th className="border px-2 py-1">Действие</th>
          </tr>
        </thead>
        <tbody>
          {norms.map(n => (
            <tr key={n.id} className="border-t">
              <td className="border px-2 py-1">
                <input defaultValue={n.job} onBlur={(e) => updateNorm(n.id, "job", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input defaultValue={n.category} onBlur={(e) => updateNorm(n.id, "category", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input defaultValue={n.brand} onBlur={(e) => updateNorm(n.id, "brand", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input type="number" defaultValue={n.max} onBlur={(e) => updateNorm(n.id, "max", e.target.value)} className="border px-1 w-16" />
              </td>
              <td className="border px-2 py-1">
                <button onClick={() => deleteNorm(n.id)} className="text-red-600 hover:underline">Удалить</button>
              </td>
            </tr>
          ))}

          <tr className="border-t bg-gray-50">
            <td className="border px-2 py-1">
              <input value={newNorm.job} onChange={(e) => setNewNorm({ ...newNorm, job: e.target.value })} className="border px-1 w-full" />
            </td>
            <td className="border px-2 py-1">
              <input value={newNorm.category} onChange={(e) => setNewNorm({ ...newNorm, category: e.target.value })} className="border px-1 w-full" />
            </td>
            <td className="border px-2 py-1">
              <input value={newNorm.brand} onChange={(e) => setNewNorm({ ...newNorm, brand: e.target.value })} className="border px-1 w-full" />
            </td>
            <td className="border px-2 py-1">
              <input type="number" value={newNorm.max} onChange={(e) => setNewNorm({ ...newNorm, max: e.target.value })} className="border px-1 w-16" />
            </td>
            <td className="border px-2 py-1">
              <button onClick={addNorm} className="text-blue-600 hover:underline">Добавить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
