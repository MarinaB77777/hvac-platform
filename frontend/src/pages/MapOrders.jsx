import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function MapOrders() {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    API.get("/orders/available")
      .then(res => setOrders(res.data))
      .catch(() => alert("Ошибка загрузки заказов"))
  }, [])

  const takeOrder = async (id) => {
    try {
      await API.post(`/orders/${id}/take`)
      alert("Вы приняли заказ. Ожидается оплата клиента.")
      setOrders((prev) => prev.filter(o => o.id !== id))
    } catch {
      alert("Не удалось принять заказ")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Свободные заказы</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">Нет доступных заказов</p>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div key={order.id} className="border p-4 rounded">
              <div><b>Имя клиента:</b> {order.client_name || "не указано"}</div>
              <div><b>Адрес:</b> {order.address}</div>
              <div><b>Описание:</b> {order.description}</div>
              <button
                onClick={() => takeOrder(order.id)}
                className="mt-2 bg-green-600 text-white px-4 py-1 rounded"
              >
                Принять заказ
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
