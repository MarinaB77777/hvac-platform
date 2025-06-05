from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    role: str = "hvac"  # можно оставить фиксированной

await axios.post('https://hvac-platform.onrender.com/register', {
  name: username,     // ← это отображаемое имя
  phone: username,    // ← это же используется как логин
  password: password,
  role: 'hvac'
});
