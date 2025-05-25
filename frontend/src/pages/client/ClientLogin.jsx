import { useState } from "react";
import axios from "axios";

export default function ClientLogin() {
  const [phone, setPhone] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/login", new URLSearchParams({
        username: phone,
        password: "unused"
      }));
      localStorage.setItem("token", response.data.access_token);
      window.location.href = "/client-orders";
    } catch (err) {
      alert("Ошибка входа");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-xl mb-4">Вход клиента</h1>
      <input
        type="text"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="Телефон"
        className="border p-2 w-full mb-4"
      />
      <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2">
        Войти
      </button>
    </div>
  );
}
