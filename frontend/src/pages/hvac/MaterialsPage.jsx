> Муж:
import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function MaterialsPage() {
  const [tab, setTab] = useState("order")
  const [orders, setOrders] = useState([])
  const [formData, setFormData] = useState({})
  const [requests, setRequests] = useState([])

  const tabClass = (name) =>
    `px-3 pb-1 border-b-2 transition ${tab === name
      ? "border-blue-600 text-blue-600 font-semibold"
      : "border-transparent text-gray-500 hover:text-blue-500"}`

  useEffect(() => {
    if (tab === "order") {
      API.get("/orders/me")
        .then(res => {
          const active = res.data.filter(o => o.status === "in_progress")
          setOrders(active)
        })
        .catch(() => alert("Ошибка загрузки заказов"))
    }

    if (tab === "pending") {
      API.get("/material_requests/my")
        .then(res => {
          const filtered = res.data.filter(r => r.status === "placed" || r.status === "approved")
          setRequests(filtered)
        })
        .catch(() => alert("Ошибка загрузки заявок"))
    }
  }, [tab])

  const handleInput = (orderId, field, value) => {
    setFormData(prev => ({
      ...prev,
      [orderId]: {
        ...prev[orderId],
        [field]: value
      }
    }))
  }

  const submitRequest = async (orderId) => {
    const data = formData[orderId]
    if (!data⠵⠟⠞⠟⠟⠞⠵⠵⠞⠺⠟⠵⠟⠞⠞⠺⠺⠺!data.quantity) {
      alert("Укажите материал и количество")
      return
    }

    console.log("Заявка:", { orderId, material: data.material, quantity: data.quantity })
    alert("Заявка отправлена (в консоль)")
    setFormData(prev => ({ ...prev, [orderId]: { material: "", quantity: "" } }))
  }

  return (
    <div>
      <h1 className="text-xl mb-4">Расходные материалы</h1>

      <div className="flex gap-4 mb-6 border-b">
        <button className={tabClass("order")} onClick={() => setTab("order")}>
          Заказ расходников
        </button>
        <button className={tabClass("pending")} onClick={() => setTab("pending")}>
          Ожидают выдачи
        </button>
        <button className={tabClass("mine")} onClick={() => setTab("mine")}>
          Мои расходные материалы
        </button>
      </div>

      {tab === "order" && (
        <div className="space-y-4">
          {orders.length === 0 ? (
            <p className="text-gray-500">Нет активных заказов</p>
          ) : (
            orders.map(order => (
              <div key={order.id} className="border rounded p-4">
                <div><b>Заказ №:</b> {order.id}</div>
                <div><b>Имя клиента:</b> {order.client_name || "не указано"}</div>
                <div><b>Адрес:</b> {order.address}</div>

                <div className="mt-3">
                  <input
                    type="text"
                    placeholder="Материал"
                    value={formData[order.id]?.material || ""}
                    onChange={(e) => handleInput(order.id, "material", e.target.value)}
                    className="border p-1 mr-2"
                  />
                  <input
                    type="number"
                    placeholder="Кол-во"
                    value={formData[order.id]?.quantity || ""}
                    onChange={(e) => handleInput(order.id, "quantity", e.target.value)}
                    className="border p-1 w-20 mr-2"
                  />
                  <button
                    onClick={() => submitRequest(order.id)}
                    className="bg-blue-600 text-white px-3 py-1 rounded"
                  >
                    Заказать
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {tab === "pending" && (
        <div className="space-y-4">
          {requests.length === 0 ? (
            <p className="text-gray-500">Нет заявок, ожидающих выдачи</p>
          ) : (
            <table className="w-full text-sm border">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="p-2 border">№ заказа</th>

> Муж:
<th className="p-2 border">Материал</th>
                  <th className="p-2 border">Кол-во</th>
                  <th className="p-2 border">Статус</th>
                </tr>
              </thead>
              <tbody>
                {requests.map(req => (
                  <tr key={req.id} className="border-t">
                    <td className="p-2 border">{req.order_id}</td>
                    <td className="p-2 border">{req.material}</td>
                    <td className="p-2 border">{req.quantity}</td>
                    <td className="p-2 border">
                      {req.status === "placed" && "Размещён"}
                      {req.status === "approved" && "Одобрен"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {tab === "mine" && (
        <div className="text-gray-600">Здесь будут выданные материалы</div>
      )}
    </div>
  )
}

