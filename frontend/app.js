const API_URL = `${window.location.protocol}//${window.location.hostname}:8000`;

const statusEl = document.getElementById('status');
const taskListEl = document.getElementById('task-list');
const taskFormEl = document.getElementById('task-form');
const titleEl = document.getElementById('title');
const descriptionEl = document.getElementById('description');

async function fetchTasks() {
  statusEl.textContent = 'Оновлюємо список задач...';
  const response = await fetch(`${API_URL}/tasks`);
  const tasks = await response.json();
  renderTasks(tasks);
  statusEl.textContent = `Знайдено задач: ${tasks.length}`;
}

function renderTasks(tasks) {
  taskListEl.innerHTML = '';

  if (tasks.length === 0) {
    taskListEl.innerHTML = '<p>Поки що задач немає.</p>';
    return;
  }

  tasks.forEach((task) => {
    const taskEl = document.createElement('div');
    taskEl.className = `task ${task.completed ? 'completed' : ''}`;

    taskEl.innerHTML = `
      <div>
        <h3>${escapeHtml(task.title)}</h3>
        <p>${escapeHtml(task.description || 'Без опису')}</p>
        <small>${task.completed ? 'Виконано' : 'Активна'}</small>
      </div>
      <div class="actions">
        <button class="secondary" data-action="toggle">${task.completed ? 'Повернути' : 'Завершити'}</button>
        <button data-action="delete">Видалити</button>
      </div>
    `;

    taskEl.querySelector('[data-action="toggle"]').addEventListener('click', async () => {
      await fetch(`${API_URL}/tasks/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed }),
      });
      fetchTasks();
    });

    taskEl.querySelector('[data-action="delete"]').addEventListener('click', async () => {
      await fetch(`${API_URL}/tasks/${task.id}`, { method: 'DELETE' });
      fetchTasks();
    });

    taskListEl.appendChild(taskEl);
  });
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

taskFormEl.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    title: titleEl.value.trim(),
    description: descriptionEl.value.trim(),
    completed: false,
  };

  await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  taskFormEl.reset();
  fetchTasks();
});

fetchTasks().catch((error) => {
  console.error(error);
  statusEl.textContent = 'Не вдалося підключитися до backend API.';
});
