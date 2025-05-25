import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerAi() {
  const [insights, setInsights] = useState([])
  const [filtered, setFiltered] = useState([])
  const [filter, setFilter] = useState("Все")
  const [settings, setSettings] = useState({
    enabled: true,
    frequency: 7,
    sensitivity: "Normal",
    notify: true
  })

  useEffect(() => {
    loadInsights()
    loadSettings()
  }, [])

  const loadInsights = async () => {
    try {
      const res = await API.get("/ai/insights")
      setInsights(res.data)
      setFiltered(res.data)
    } catch {
      // Мок-данные
      const mock = [
        {
          title: "Превышение нормы фреона",
          detail: "HVAC Иванов П. использует 3 баллона R410 на замену компрессора.",
          recommendation: "Провести проверку.",
          category: "Материалы"
        },
        {
          title: "Низкий рейтинг",
          detail: "HVAC Сидоров А. имеет среднюю оценку 2.7 за 10 заказов.",
          recommendation: "Проверить работу.",
          category: "Рейтинги"
        },
        {
          title: "Склад на нуле",
          detail: "Фильтры LG заканчиваются — менее 2 шт.",
          recommendation: "Пополнить склад.",
          category: "Склад"
        }
      ]
      setInsights(mock)
      setFiltered(mock)
    }
  }

  const loadSettings = async () => {
    try {
      const res = await API.get("/ai/settings")
      setSettings(res.data)
    } catch {
      // оставить мок
    }
  }

  const updateSetting = (field, value) => {
    const updated = { ...settings, [field]: value }
    setSettings(updated)
    API.patch("/ai/settings", updated).catch(() => {})
  }

  const handleFilter = (cat) => {
    setFilter(cat)
    if (cat === "Все") setFiltered(insights)
    else setFiltered(insights.filter(i => i.category === cat))
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">ИИ-анализ: выводы и настройки</h1>

      <div className="mb-6 border p-4 rounded bg-gray-50">
        <h2 className="font-medium mb-2">Настройки анализа</h2>
        <div className="flex gap-4 flex-wrap text-sm">
          <label>
            <input
              type="checkbox"
              checked={settings.enabled}
              onChange={(e) => updateSetting("enabled", e.target.checked)}
              className="mr-1"
            />
            Включить ИИ-анализ
          </label>
          <label>
            Частота анализа (дней):
            <input
              type="number"
              value={settings.frequency}
              onChange={(e) => updateSetting("frequency", e.target.value)}
              className="ml-2 border px-1 w-16"
            />
          </label>
          <label>
            Чувствительность:
            <select
              value={settings.sensitivity}
              onChange={(e) => updateSetting("sensitivity", e.target.value)}
              className="ml-2 border"
            >
              <option>Low</option>
              <option>Normal</option>
              <option>High</option>
            </select>
          </label>
          <label>
            <input
              type="checkbox"
              checked={settings.notify}
              onChange={(e) => updateSetting("notify", e.target.checked)}
              className="mr-1"
            />
            Уведомлять о нарушениях
          </label>
        </div>
      </div>

      <div className="mb-4 flex gap-4 items-center text-sm">
        <span className="text-gray-600">Фильтр по категории:</span>
        {["Все", "Материалы", "Рейтинги", "Склад"].map(cat => (
          <button
            key={cat}
            onClick={() => handleFilter(cat)}
            className={`px-3 py-1 rounded border ${
              filter === cat ? "bg-blue-600 text-white" : "bg-white text-gray-800"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <p className="text-gray-500">Нет данных для выбранной категории</p>
      ) : (

<div className="space-y-4">
          {filtered.map((i, idx) => (
            <div key={idx} className="border rounded p-4 bg-white shadow-sm">
              <h2 className="font-bold text-lg mb-1 text-red-600">{i.title}</h2>
              <p className="mb-2 text-gray-800">{i.detail}</p>
              <p className="text-sm text-green-700"><b>Рекомендация:</b> {i.recommendation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

