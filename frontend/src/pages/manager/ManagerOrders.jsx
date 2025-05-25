import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerOrders() {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    loadOrders()
  }, [])

  const loadOrders = async () => {
    try {
      const res = await API.get("/orders/all")
      setOrders(res.data)
    } catch {
      alert("Ошибка загрузки заказов")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Все заказы (HVAC)</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">Нет заказов</p>
      ) : (
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Дата</th>
              <th className="border px-2 py-1">Клиент</th>
              <th className="border px-2 py-1">Адрес</th>
              <th className="border px-2 py-1">HVAC</th>
              <th className="border px-2 py-1">Статус</th>
              <th className="border px-2 py-1">Диагностика</th>
              <th className="border px-2 py-1">Ремонт</th>
              <th className="border px-2 py-1">Материалы</th>
              <th className="border px-2 py-1">Оценка</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id} className="border-t">
                <td className="border px-2 py-1">{order.date}</td>
                <td className="border px-2 py-1">{order.client_name}</td>
                <td className="border px-2 py-1">{order.address}</td>
                <td className="border px-2 py-1">{order.hvac_name}</td>
                <td className="border px-2 py-1">{order.status}</td>
                <td className="border px-2 py-1">${order.diagnostic_fee}</td>
                <td className="border px-2 py-1">${order.repair_fee}</td>
                <td className="border px-2 py-1">{order.materials_used?.join(", ") || "-"}</td>
                <td className="border px-2 py-1">{order.rating || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
