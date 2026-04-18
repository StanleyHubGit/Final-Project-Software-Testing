import api from "../api/apiClient";

export default function AssignmentCard({ task, onUpdate }) {
  const getStatusStyle = (status) => {
    switch (status) {
      case "pending":
        return { backgroundColor: "#ffeaa7" };
      case "submitted":
        return { backgroundColor: "#55efc4" };
      case "late":
        return { backgroundColor: "#ff7675", color: "white" };
      default:
        return {};
    }
  };

  const handleSubmit = async () => {
    try {
      await api.put(`/tasks/${task.id}/status`, {
        status: "submitted",
      });

      alert("Tugas disubmit!");
      onUpdate();
    } catch (err) {
      console.error(err);
      alert("Gagal update");
    }
  };

  return (
    <div className="card">
      <h4>{task.title}</h4>

      <span
        style={{
          padding: "5px 10px",
          borderRadius: "5px",
          fontSize: "12px",
          ...getStatusStyle(task.status),
        }}
      >
        {task.status}
      </span>

      {task.status !== "submitted" && (
        <button onClick={handleSubmit}>Submit</button>
      )}
    </div>
  );
}