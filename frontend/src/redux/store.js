/**
 * Redux store configuration.
 */
import { configureStore } from '@reduxjs/toolkit';
import interactionReducer from './slices/interactionSlice';

export const store = configureStore({
  reducer: {
    interaction: interactionReducer
  }
});
