import { API_BASE_URL } from '@/constants/urls';

export const getLaboratories = async () => {
  const response = await fetch(`${API_BASE_URL}/lab/laboratories/`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch laboratories');
  }

  const data = await response.json();
  console.log('Response data:', data);  // Verificación de la respuesta en consola
  return data;
};
