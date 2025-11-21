import React from 'react';

function TodoItem({ todo, onToggleComplete, onDeleteTodo }) {
  const itemStyle = {
    display: 'flex',
    alignItems: 'center',
    padding: '10px',
    borderBottom: '1px #ddd solid',
    textDecoration: todo.completed ? 'line-through' : 'none',
    backgroundColor: todo.completed ? '#f0f0f0' : '#ffffff',
    margin: '5px 0',
    borderRadius: '4px'
  };

  const titleStyle = {
    flexGrow: 1,
    marginLeft: '10px',
    color: todo.completed ? '#888' : '#333'
  };

  const deleteButtonStyle = {
    background: '#ff4d4d',
    color: '#fff',
    border: 'none',
    padding: '6px 10px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '0.8em',
    marginLeft: '10px'
  };

  const checkboxStyle = {
    transform: 'scale(1.2)'
  };

  return (
    <div style={itemStyle}>
      <input
        type="checkbox"
        style={checkboxStyle}
        checked={todo.completed}
        onChange={() => onToggleComplete(todo.id)}
      />
      <span style={titleStyle}>{todo.title}</span>
      <button onClick={() => onDeleteTodo(todo.id)} style={deleteButtonStyle}>
        Delete
      </button>
    </div>
  );
}

export default TodoItem;