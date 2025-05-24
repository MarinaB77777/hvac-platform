import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function MaterialsPage() {
  const [tab, setTab] = useState("order")
  const [orders, setOrders] = useState([])

  const tabClass = (name) =>
    `px-3 pb-1 border-b-2 transition ${tab === name
      ? "border-blue-600 text-blue-600 font-semibold"
      : "border-transparent text-gray-500 hover:text-blue-500"}`

  useEffect(() => {
    if (tab === "order") {
      API.get("/orders/me")
        .then(res => {
          const inProgressOrders = res.data.filter(o => o.status === "in_progress")
          setOrders(inProgressOrders)
        })
        .catch(() => alert("Ошибка загрузки заказов"))
    }
  }, [tab])

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
            <p className="text-gray-500">Нет активных заказов для оформления заявок</p>
          ) : (
            orders.map(order => (
              <div key={order.id} className="border rounded p-4">
                <div><b>Заказ №:</b> {order.id}</div>
                <div><b>Имя клиента:</b> {order.client_name || "не указано"}</div>
                <div><b>Адрес:</b> {order.address}</div>
                <button className="mt-3 bg-blue-600 text-white px-4 py-1 rounded">
                  Добавить расходники
                </button>
              </div>
            ))
          )}
        </div>
      )}

      {tab === "pending" && (
        <div className="text-gray-600">Здесь будет таблица заявок в статусе "Размещён" или "Одобрен"</div>
      )}

      {tab === "mine" && (
        <div className="text-gray-600">Здесь будут выданные материалы</div>
      )}
    </div>
  )
}
