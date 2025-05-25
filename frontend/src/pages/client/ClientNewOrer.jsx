import { useState } from "react"
import { useNavigate } from "react-router-dom"
import API from "../../api/axios"

export default function ClientNewOrder() {
  const [form, setForm] = useState({
    name: "",
    phone: "",
    address: "",
    description: ""
  })

  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const submitOrder = async () => {
    if (!form.name!form.address || !form.description) {
      alert("Пожалуйста, заполните все поля")
      return
    }

    try {
      await API.post("/orders/create", form)
      alert("Заказ отправлен. Ожидайте подтверждения.")
      navigate("/client/orders")
    } catch {
      alert("Ошибка при создании заказа")
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-xl mb-4">Создание заказа</h1>
      <input
        name="name"
        placeholder="Имя"
        value={form.name}
        onChange={handleChange}
        className="border p-2 w-full mb-3"
      />
      <input
        name="phone"
        placeholder="Телефон"
        value={form.phone}
        onChange={handleChange}
        className="border p-2 w-full mb-3"
      />
      <input
        name="address"
        placeholder="Адрес"
        value={form.address}
        onChange={handleChange}
        className="border p-2 w-full mb-3"
      />
      <textarea
        name="description"
        placeholder="Что сломалось?"
        value={form.description}
        onChange={handleChange}
        className="border p-2 w-full mb-3"
      />
      <button
        onClick={submitOrder}
        className="bg-blue-600 text-white px-4 py-2 w-full"
      >
        Отправить заказ
      </button>
    </div>
  )
}
