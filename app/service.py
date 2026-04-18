from app.model import tasks, task_id_counter

def create_task(title):
    global task_id_counter
    
    if not title or title.strip() == "":
        raise ValueError("Title cannot be empty")
    
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }
    
    tasks.append(task)
    return task


def get_all_tasks():
    return tasks


def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False