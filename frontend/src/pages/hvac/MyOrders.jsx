import { useEffect, useState } from "react"
import API from "../../api/axios"

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
  const [showForm, setShowForm] = useState({})
  const [urlInput, setUrlInput] = useState("")

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

  const submitUpload = async (orderId) => {
    const type = showForm[orderId]
    if (!urlInput.trim()) return alert("Введите ссылку")

    if (type === "diagnostic") {
      await API.post(`/orders/${orderId}/upload-diagnostic`, { url: urlInput })
    } else if (type === "result") {
      await API.post(`/orders/${orderId}/upload-result`, { url: urlInput })
    }

    setShowForm(prev => ({ ...prev, [orderId]: null }))
    setUrlInput("")
    loadOrders()
  }

  const rateOrder = async (id) => {
    const rating = prompt("Оцените заказ (1–5):")
    if (rating && !isNaN(rating)) {
      await API.post(`/orders/${id}/rate`, { rating: Number(rating) })
      loadOrders()
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Мои заказы</h1>
      {orders.map(order => (
        <div key={order.id} className="border p-4 mb-4 rounded">
          <div><b>Адрес:</b> {order.address}</div>
          <div><b>Статус:</b> {order.status}</div>
          <div><b>Таймер:</b> {formatDuration(order.started_at)}</div>

          {showForm[order.id] && (
            <div className="mt-2">
              <input
                type="text"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="Вставьте ссылку на файл"
                className="border px-2 py-1 w-full mb-2"
              />
              <button
                onClick={() => submitUpload(order.id)}
                className="bg-blue-700 text-white px-3 py-1"
              >
                Отправить
              </button>
            </div>
          )}

          {order.status === "accepted" && (
            <>
              <button
                onClick={() => setShowForm({ [order.id]: "diagnostic" })}
                className="bg-blue-500 text-white px-3 py-1 mt-2 mr-2"
              >
                Загрузить диагностику
              </button>
              <button
                onClick={() => updateStatus(order.id, "in_progress")}
                className="bg-yellow-500 text-white px-3 py-1 mt-2"
              >
                В работу
              </button>
            </>
          )}

          {order.status === "in_progress" && (
            <>
              <button
                onClick={() => setShowForm({ [order.id]: "result" })}
                className="bg-blue-600 text-white px-3 py-1 mt-2 mr-2"
              >
                Загрузить результат
              </button>
              <button
                onClick={() => updateStatus(order.id, "completed")}
                className="bg-green-600 text-white px-3 py-1 mt-2"
              >
                Завершить
              </button>
            </>
          )}

          {order.status === "completed" && (
            <button
              onClick={() => rateOrder(order.id)}
              className="bg-purple-600 text-white px-3 py-1 mt-2"
            >
              Оценить заказ
            </button>
          )}
        </div>
      ))}
    </div>
  )
}
