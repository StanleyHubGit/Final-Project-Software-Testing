import { useRef } from "react";
import AssignmentForm from "../components/AssignmentForm";
import AssignmentList from "../components/AssignmentList";

export default function Dashboard() {
  const listRef = useRef();

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="container">
      <h1>Dashboard</h1>

      <button className="logout" onClick={handleLogout}>
        Logout
      </button>

      <div className="card">
        <AssignmentForm onSuccess={() => listRef.current.fetchTasks()} />
      </div>

      <div className="card">
        <AssignmentList ref={listRef} />
      </div>
    </div>
  );
}