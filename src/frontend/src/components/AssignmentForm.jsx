import { useState } from "react";
import api from "../api/apiClient";

export default function AssignmentForm({ onSuccess }) {
  const [title, setTitle] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title.trim()) {
      alert("Judul tidak boleh kosong");
      return;
    }

    try {
      await api.post(
        "/tasks/",
        {
          title,
          user_id: 1,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      alert("Task berhasil dibuat");
      setTitle("");

      onSuccess(); // 🔥 refresh otomatis
    } catch (err) {
      console.error(err);
      alert("Gagal membuat task");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Tambah Assignment</h3>

      <input
        type="text"
        placeholder="Judul tugas"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <button type="submit">Tambah</button>
    </form>
  );
}