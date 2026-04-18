import { useState } from "react";
import api from "../api/apiClient";
import { useNavigate } from "react-router-dom";

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post(
        "/auth/register",
        {
          email,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json", // 🔥 DI SINI AXIOS DIPERBAIKI
          },
        }
      );

      alert("Register berhasil!");
      navigate("/");
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Register gagal");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Register</button>
    </form>
  );
}