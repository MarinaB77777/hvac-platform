import { useEffect, useState } from "react"
import API from "../api/axios"

function formatDuration(startedAt) {
  if (!startedAt) return "-"
  const start = new Date(startedAt)
  const now = new Date()
  const diff = Math.floor((now - start) / 1000)
  const min = Math.floor(diff / 60)
  const sec = diff % 60
  return ${min}м ${sec}с
}

export default function MyOrders() {
  const [orders, setOrders] = useState([])

  const loadOrders = async () => {
    const res = await API.get("/orders/me")
    setOrders(res.data.filter(o => o.status !== "new"))
  }

  useEffect(() => {
    loadOrders()
    const interval = setInterval(loadOrders, 5000)
    return () => clearInterval(interval)
  }, [])

  const updateStatus = async (id, status) => {
    await API.patch(`/orders/${id}/status`, { status })
    loadOrders()
  }

  const uploadResult = async (id, url) => {
    await API.post(`/orders/${id}/upload-result`, { url })
    loadOrders()
  }

  const uploadDiagnostic = async (id, url) => {
    await API.post(`/orders/${id}/upload-diagnostic`, { url })
    loadOrders()
  }

  const rateOrder = async (id, rating) => {
    await API.post(`/orders/${id}/rate`, { rating: Number(rating) })
    loadOrders()
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Мои заказы</h1>
      {orders.map(order => (
        <div key={order.id} className="border p-4 mb-2">
          <div><b>Адрес:</b> {order.address}</div>
          <div><b>Статус:</b> {order.status}</div>
          <div><b>Таймер:</b> {formatDuration(order.started_at)}</div>

          {order.status === "accepted" && (
            <button
              onClick={() => updateStatus(order.id, "in_progress")}
              className="bg-yellow-500 text-white px-3 py-1 mt-2"
            >
              В работу
            </button>
          )}

          {order.status === "in_progress" && (
            <button
              onClick={() => updateStatus(order.id, "completed")}
              className="bg-green-600 text-white px-3 py-1 mt-2"
            >
              Завершить
            </button>
          )}
        </div>
      ))}
    </div>
  )
}
