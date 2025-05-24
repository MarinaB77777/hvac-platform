import { useState } from "react"

export default function MaterialsPage() {
  const [tab, setTab] = useState("order") // order | pending | mine

  return (
    <div>
      <h1 className="text-xl mb-4">Расходные материалы</h1>

      {/* Вкладки */}
      <div className="flex gap-4 mb-6 border-b pb-2">
        <button
          className={tab === "order" ? "font-bold text-blue-600" : ""}
          onClick={() => setTab("order")}
        >
          Заказ расходников
        </button>
        <button
          className={tab === "pending" ? "font-bold text-blue-600" : ""}
          onClick={() => setTab("pending")}
        >
          Ожидают выдачи
        </button>
        <button
          className={tab === "mine" ? "font-bold text-blue-600" : ""}
          onClick={() => setTab("mine")}
        >
          Мои расходные материалы
        </button>
      </div>

      {/* Содержимое вкладки */}
      {tab === "order" && (
        <div>Здесь будет форма выбора и заказа материалов</div>
      )}
      {tab === "pending" && (
        <div>Здесь будет таблица заявок в статусе "Размещён" или "Одобрен"</div>
      )}
      {tab === "mine" && (
        <div>Здесь будут выданные материалы</div>
      )}
    </div>
  )
}
