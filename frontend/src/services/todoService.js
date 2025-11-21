import axios from 'axios';

const API_BASE_URL = '/api/v1/todos';

export const getAllTodos = async () => {
  try {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching all todos:', error);
    throw error;
  }
};

export const getTodoById = async (id) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching todo with ID ${id}:`, error);
    throw error;
  }
};

export const createTodo = async (title) => {
  try {
    const response = await axios.post(API_BASE_URL, { title });
    return response.data;
  } catch (error) {
    console.error(`Error creating todo with title "${title}":`, error);
    throw error;
  }
};

export const updateTodo = async (id, data) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/${id}`, data);
    return response.data;
  } catch (error) {
    console.error(`Error updating todo with ID ${id}:`, error);
    throw error;
  }
};

export const deleteTodo = async (id) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting todo with ID ${id}:`, error);
    throw error;
  }
};