import {
  useEffect,
  useState,
  forwardRef,
  useImperativeHandle,
} from "react";
import api from "../api/apiClient";
import AssignmentCard from "./AssignmentCard";

const AssignmentList = forwardRef((props, ref) => {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    try {
      const res = await api.get("/tasks/?user_id=1");
      setTasks(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  useImperativeHandle(ref, () => ({
    fetchTasks,
  }));

  return (
    <div>
      <h3>Daftar Assignment</h3>

      {tasks.length === 0 ? (
        <p>Tidak ada tugas</p>
      ) : (
        tasks.map((task) => (
          <AssignmentCard key={task.id} task={task} onUpdate={fetchTasks} />
        ))
      )}
    </div>
  );
});

export default AssignmentList;