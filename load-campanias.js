import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomString, randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// export const options = {
//   stages: [
//     { duration: '10s', target: 10 }, // Calentamiento gradual (100 requests aprox)
//     { duration: '40s', target: 25 }, // Carga principal (900 requests aprox)
//     { duration: '10s', target: 0 },  // Finalización gradual

//   ],
//   thresholds: {
//     http_req_duration: ['p(95)<2000'], // 95% de requests < 2s
//     http_req_failed: ['rate<0.05'],    // Error rate < 5%
//   },
// };
export const options = {
  iterations: 4000,          // Exactamente 1000 requests
  vus: 150,                   // 20 usuarios virtuales concurrentes
  duration: '180s',          // Timeout máximo (si tarda más de 2min, algo está mal)

  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% de requests < 2s
    http_req_failed: ['rate<0.10'],    // Error rate < 5%
    iteration_duration: ['avg<4000'],  // Duración promedio por iteración < 3s
  },
};

// const BASE_URL = 'http://localhost:8004';
const BASE_URL = 'http://34.42.176.61';

export default function () {
  const payload = JSON.stringify({
    nombre: `Campaña Test ${randomString(8)}`,
    descripcion: `Campaña de prueba de carga - ${new Date().toISOString()}`,
    fecha_inicio: "2024-01-01T00:00:00Z",
    fecha_fin: "2024-12-31T23:59:59Z",
    tipo: "DIGITAL",
    edad_minima: 18,
    edad_maxima: 65,
    genero: "TODOS",
    ubicacion: "Colombia",
    intereses: ["tecnologia", "marketing", "negocios"],
    presupuesto: randomIntBetween(1000, 50000),
    canales: ["WEB", "EMAIL", "SOCIAL"]
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(`${BASE_URL}/api/v1/marketing/campanias`, payload, params);

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 2000ms': (r) => r.timings.duration < 2000,
    'response contains message': (r) => r.body.includes('procesamiento'),
  });

  sleep(1);
}