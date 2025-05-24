import { useState } from "react"
import API from "../api/axios"
import { useNavigate } from "react-router-dom"
import { getUserRole } from "../auth/auth"

export default function LoginPage() {
  const [phone, setPhone] = useState("")
  const navigate = useNavigate()

  const login = async () => {
    try {
      const res = await API.post("/login", new URLSearchParams({
        username: phone,
        password: "unused"
      }))
      localStorage.setItem("token", res.data.access_token)
      const role = getUserRole()
      if (role === "client") navigate("/client")
      else if (role === "hvac") navigate("/hvac")
      else if (role === "warehouse") navigate("/warehouse")
      else if (role === "manager") navigate("/manager")
      else navigate("/")
    } catch (err) {
      alert("Ошибка входа")
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-xl mb-4">Вход</h1>
      <input
        type="text"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="Телефон"
        className="border p-2 w-full mb-4"
      />
      <button onClick={login} className="bg-blue-600 text-white px-4 py-2 w-full">
        Войти
      </button>
    </div>
  )
}
