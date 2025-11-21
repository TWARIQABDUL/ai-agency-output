import React from 'react';
import TodoItem from './TodoItem';

function TodoList({ todos, onToggleComplete, onDeleteTodo }) {
  return (
    <div className="todo-list">
      {todos?.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggleComplete={onToggleComplete}
          onDeleteTodo={onDeleteTodo}
        />
      ))}
    </div>
  );
}

export default TodoList;