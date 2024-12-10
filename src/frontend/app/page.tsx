// app/page.tsx
"use client";

import { useEffect, useState } from 'react';
import axios from 'axios';

const Page = () => {
  const [data, setData] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Укажите URL вашего FastAPI сервера
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

    axios
      .get(`${API_URL}/api/data`)
      .then((response) => {
        setData(response.data.message); // Извлекаем поле "message" из ответа
      })
      .catch((err) => {
        console.error("Ошибка при запросе:", err);
        setError("Не удалось получить данные от сервера.");
      });
  }, []);

  return (
    <main style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Проверка связи с FastAPI</h1>
      {error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : data ? (
        <p>Ответ от сервера: <strong>{data}</strong></p>
      ) : (
        <p>Загрузка данных...</p>
      )}
    </main>
  );
};

export default Page;
