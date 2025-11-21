import React, { useState } from 'react';

function AddTodoForm({ onAddTodo }) {
  const [todoTitle, setTodoTitle] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (todoTitle.trim() === '') {
      return; // Do not submit empty todos
    }
    onAddTodo(todoTitle);
    setTodoTitle(''); // Clear the input field
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="todoTitleInput">Todo Title:</label>
      <input
        id="todoTitleInput"
        type="text"
        placeholder="Enter new todo title"
        value={todoTitle}
        onChange={(e) => setTodoTitle(e.target.value)}
      />
      <button type="submit">Add Todo</button>
    </form>
  );
}

export default AddTodoForm;