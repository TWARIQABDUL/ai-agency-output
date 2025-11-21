import React, { useState, useEffect } from 'react';
import DOMPurify from 'dompurify';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTodoText, setNewTodoText] = useState('');

  const API_BASE_URL = '/api/todos';

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(API_BASE_URL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setTodos(data);
      } catch (e) {
        setError("Failed to fetch todos: " + e.message);
        console.error("Fetch error:", e);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, []);

  const addTodo = async (e) => {
    e.preventDefault();
    if (!newTodoText.trim()) return;

    try {
      const cleanNewTodoText = DOMPurify.sanitize(newTodoText, { USE_PROFILES: { html: false } });
      if (!cleanNewTodoText.trim()) {
        setNewTodoText('');
        return;
      }

      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: cleanNewTodoText, completed: false }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const newTodo = await response.json();
      setTodos((prevTodos) => [...prevTodos, newTodo]);
      setNewTodoText('');
    } catch (e) {
      setError("Failed to add todo: " + e.message);
      console.error("Add todo error:", e);
    }
  };

  const toggleTodoCompletion = async (id) => {
    const todoToToggle = todos.find((todo) => todo.id === id);
    if (!todoToToggle) return;

    const updatedTodo = { ...todoToToggle, completed: !todoToToggle.completed };

    try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedTodo),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const returnedUpdatedTodo = await response.json();
      setTodos((prevTodos) =>
        prevTodos.map((todo) => (todo.id === id ? returnedUpdatedTodo : todo))
      );
    } catch (e) {
      setError("Failed to update todo: " + e.message);
      console.error("Toggle todo error:", e);
    }
  };

  const deleteTodo = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setTodos((prevTodos) => prevTodos.filter((todo) => todo.id !== id));
    } catch (e) {
      setError("Failed to delete todo: " + e.message);
      console.error("Delete todo error:", e);
    }
  };

  if (loading) {
    return <div>Loading todos...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Todo List</h1>

      <form onSubmit={addTodo} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={newTodoText}
          onChange={(e) => setNewTodoText(e.target.value)}
          placeholder="Add a new todo"
          style={{ padding: '8px', marginRight: '10px', width: '70%' }}
        />
        <button type="submit" style={{ padding: '8px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}>
          Add Todo
        </button>
      </form>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map((todo) => (
          <li
            key={todo.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: '10px',
              padding: '10px',
              border: '1px solid #eee',
              borderRadius: '5px',
              backgroundColor: todo.completed ? '#f9f9f9' : 'white',
            }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodoCompletion(todo.id)}
              style={{ marginRight: '10px' }}
            />
            <span
              dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(todo.text) }}
              style={{
                flexGrow: 1,
                textDecoration: todo.completed ? 'line-through' : 'none',
                color: todo.completed ? '#888' : '#333',
              }}
            >
            </span>
            <button
              onClick={() => deleteTodo(todo.id)}
              style={{
                padding: '5px 10px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                cursor: 'pointer',
                borderRadius: '3px',
              }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;