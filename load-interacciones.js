import http from 'k6/http';
import { check } from 'k6';

// Simple test configuration - 100 requests total
export const options = {
  vus: 10,        // 10 virtual users
  iterations: 1000, // Total 100 requests
};

// const BASE_URL = 'http://localhost:8004';
const BASE_URL = 'http://34.42.176.61';

// Generate simple test data for interaction
function generateInteractionData() {
  const tipos = ['CLICK', 'VIEW'];
  const usuarios = ['user1', 'user2', 'user3', 'user4', 'user5'];
  const elementos = ['button-cta', 'banner-home', 'form-contact', 'link-product', 'menu-nav'];
  
  return {
    tipo: tipos[Math.floor(Math.random() * tipos.length)],
    marca_temporal: new Date().toISOString(),
    identidad_usuario: usuarios[Math.floor(Math.random() * usuarios.length)],
    parametros_tracking: {
      page: '/home',
      session_id: `session_${Math.random().toString(36).substring(7)}`,
      user_agent: 'k6-test'
    },
    elemento_objetivo: elementos[Math.floor(Math.random() * elementos.length)],
    contexto: {
      campaign_id: `camp_${Math.floor(Math.random() * 1000)}`,
      source: 'web',
      device: 'desktop'
    }
  };
}

export default function () {
  const interactionData = generateInteractionData();
  
  const headers = {
    'Content-Type': 'application/json',
  };

  const response = http.post(
    `${BASE_URL}/api/v1/tracking/interaccion`,
    JSON.stringify(interactionData),
    { headers: headers }
  );

  // Simple checks
  check(response, {
    'status is 200': (r) => r.status === 200,
    'has correlation id': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.id_correlacion && body.id_correlacion.length > 0;
      } catch (e) {
        return false;
      }
    },
  });

  console.log(`Request completed - Status: ${response.status}`);
}