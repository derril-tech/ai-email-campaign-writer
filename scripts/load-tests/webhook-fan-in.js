import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '1m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<100'], // 95% of requests must complete below 100ms
    http_req_failed: ['rate<0.02'],   // Error rate must be less than 2%
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api/v1';

export default function () {
  const headers = {
    'Content-Type': 'application/json',
  };

  // Simulate various webhook events
  const webhookEvents = [
    {
      event: 'email.delivered',
      campaign_id: 'test-campaign-1',
      recipient_id: `recipient-${Date.now()}`,
      timestamp: new Date().toISOString(),
    },
    {
      event: 'email.opened',
      campaign_id: 'test-campaign-1',
      recipient_id: `recipient-${Date.now()}`,
      timestamp: new Date().toISOString(),
    },
    {
      event: 'email.clicked',
      campaign_id: 'test-campaign-1',
      recipient_id: `recipient-${Date.now()}`,
      url: 'https://example.com/click',
      timestamp: new Date().toISOString(),
    },
    {
      event: 'email.bounced',
      campaign_id: 'test-campaign-1',
      recipient_id: `recipient-${Date.now()}`,
      reason: 'hard_bounce',
      timestamp: new Date().toISOString(),
    },
    {
      event: 'email.unsubscribed',
      campaign_id: 'test-campaign-1',
      recipient_id: `recipient-${Date.now()}`,
      timestamp: new Date().toISOString(),
    },
  ];

  // Send random webhook event
  const randomEvent = webhookEvents[Math.floor(Math.random() * webhookEvents.length)];
  const webhookResponse = http.post(`${BASE_URL}/webhooks/sendgrid`, JSON.stringify(randomEvent), { headers });
  
  check(webhookResponse, {
    'webhook processing successful': (r) => r.status === 200,
    'webhook processing time < 100ms': (r) => r.timings.duration < 100,
  });

  sleep(0.1); // Very short sleep for high-frequency webhooks
}
