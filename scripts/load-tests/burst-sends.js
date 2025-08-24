import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests must complete below 200ms
    http_req_failed: ['rate<0.1'],    // Error rate must be less than 10%
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api/v1';
const AUTH_TOKEN = __ENV.AUTH_TOKEN || 'test-token';

export default function () {
  const headers = {
    'Authorization': `Bearer ${AUTH_TOKEN}`,
    'Content-Type': 'application/json',
  };

  // Test campaign creation
  const campaignData = {
    name: `Load Test Campaign ${Date.now()}`,
    subject: 'Test Subject',
    html_content: '<p>Test email content</p>',
    audience_id: 'test-audience-id',
  };

  const createResponse = http.post(`${BASE_URL}/campaigns`, JSON.stringify(campaignData), { headers });
  
  check(createResponse, {
    'campaign creation successful': (r) => r.status === 201,
    'campaign creation time < 200ms': (r) => r.timings.duration < 200,
  });

  if (createResponse.status === 201) {
    const campaignId = JSON.parse(createResponse.body).id;
    
    // Test campaign sending
    const sendResponse = http.post(`${BASE_URL}/campaigns/${campaignId}/send`, {}, { headers });
    
    check(sendResponse, {
      'campaign send successful': (r) => r.status === 200,
      'campaign send time < 500ms': (r) => r.timings.duration < 500,
    });
  }

  sleep(1);
}
