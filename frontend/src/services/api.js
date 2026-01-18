/**
 * API client for backend communication.
 */
import axios from 'axios';

// Get API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Send a chat message to the backend.
 * @param {string} message - User's natural language message
 * @param {number|null} interactionId - Optional interaction ID for editing
 * @returns {Promise} Response with form_data and chat_response
 */
export const sendMessage = async (message, interactionId = null) => {
  const response = await apiClient.post('/chat', {
    message,
    interaction_id: interactionId
  });
  return response.data;
};

/**
 * Save interaction to database.
 * @param {object} formData - Form data to save
 * @returns {Promise} Created interaction with ID
 */
export const saveInteraction = async (formData) => {
  const response = await apiClient.post('/interactions', formData);
  return response.data;
};

/**
 * Get a single interaction by ID.
 * @param {number} id - Interaction ID
 * @returns {Promise} Interaction data
 */
export const getInteraction = async (id) => {
  const response = await apiClient.get(`/interactions/${id}`);
  return response.data;
};

/**
 * Update an existing interaction.
 * @param {number} id - Interaction ID
 * @param {object} updateData - Fields to update
 * @returns {Promise} Updated interaction
 */
export const updateInteraction = async (id, updateData) => {
  const response = await apiClient.patch(`/interactions/${id}`, updateData);
  return response.data;
};

/**
 * List all interactions.
 * @returns {Promise} Array of interactions
 */
export const listInteractions = async () => {
  const response = await apiClient.get('/interactions');
  return response.data;
};

export default {
  sendMessage,
  saveInteraction,
  getInteraction,
  updateInteraction,
  listInteractions
};
