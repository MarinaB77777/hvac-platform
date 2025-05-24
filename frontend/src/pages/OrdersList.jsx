import { useEffect, useState } from "react"
import API from "../api/axios"

export default function OrdersList() {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    API.get("/orders/available")
      .then(res => setOrders(res.data))
      .catch(() => alert("Ошибка загрузки заказов"))
  }, [])

  const takeOrder = async (id) => {
    try {
      await API.post(`/orders/${id}/take`)
      setOrders((prev) => prev.filter(o => o.id !== id))
    } catch {
      alert("Не удалось принять заказ")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Доступные заказы</h1>
      {orders.length === 0 ? (
        <p>Нет заказов</p>
      ) : (
        orders.map(order => (
          <div key={order.id} className="border p-4 mb-2 rounded">
            <div><b>Адрес:</b> {order.address}</div>
            <div><b>Описание:</b> {order.description}</div>
            <button onClick={() => takeOrder(order.id)} className="mt-2 bg-green-500 text-white px-3 py-1">
              Принять
            </button>
          </div>
        ))
      )}
    </div>
  )
}
