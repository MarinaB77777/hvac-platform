import { useState } from "react"

export default function MaterialsPage() {
  const [tab, setTab] = useState("order") // order | pending | mine

  const tabClass = (name) =>
    `px-3 pb-1 border-b-2 transition ${
      tab === name
        ? "border-blue-600 text-blue-600 font-semibold"
        : "border-transparent text-gray-500 hover:text-blue-500"
    }`

  return (
    <div>
      <h1 className="text-xl mb-4">Расходные материалы</h1>

      {/* Вкладки */}
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

      {/* Содержимое вкладки */}
      {tab === "order" && (
        <div className="text-gray-600">Здесь будет форма выбора и заказа материалов</div>
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
