export default function WarehouseMovement() {
  const mock = [
    { id: 1, hvac: 2, material: "Фреон R410", qty: 2, date: "2024-05-20" },
    { id: 2, hvac: 3, material: "Фильтр Panasonic", qty: 1, date: "2024-05-21" }
  ];

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Движение на складе</h1>
      {mock.map(row => (
        <div key={row.id} className="border p-4 mb-2 text-sm">
          <div><b>Дата:</b> {row.date}</div>
          <div><b>HVAC:</b> {row.hvac}</div>
          <div><b>Материал:</b> {row.material}</div>
          <div><b>Количество:</b> {row.qty}</div>
        </div>
      ))}
    </div>
  );
}
