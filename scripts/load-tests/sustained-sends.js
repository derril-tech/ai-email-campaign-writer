import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5m', target: 50 },  // Ramp up to 50 users
    { duration: '30m', target: 50 }, // Stay at 50 users for 30 minutes
    { duration: '5m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests must complete below 200ms
    http_req_failed: ['rate<0.05'],   // Error rate must be less than 5%
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api/v1';
const AUTH_TOKEN = __ENV.AUTH_TOKEN || 'test-token';

export default function () {
  const headers = {
    'Authorization': `Bearer ${AUTH_TOKEN}`,
    'Content-Type': 'application/json',
  };

  // Test analytics endpoints
  const analyticsResponse = http.get(`${BASE_URL}/analytics/campaigns`, { headers });
  
  check(analyticsResponse, {
    'analytics retrieval successful': (r) => r.status === 200,
    'analytics retrieval time < 100ms': (r) => r.timings.duration < 100,
  });

  // Test webhook processing
  const webhookData = {
    event: 'email.delivered',
    campaign_id: 'test-campaign-id',
    recipient_id: 'test-recipient-id',
    timestamp: new Date().toISOString(),
  };

  const webhookResponse = http.post(`${BASE_URL}/webhooks/sendgrid`, JSON.stringify(webhookData), { headers });
  
  check(webhookResponse, {
    'webhook processing successful': (r) => r.status === 200,
    'webhook processing time < 50ms': (r) => r.timings.duration < 50,
  });

  sleep(2);
}
