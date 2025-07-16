import { rest } from 'msw';
import { setupServer } from 'msw/node';

export const handlers = [
  rest.get('/api/races/:year', (req, res, ctx) => {
    return res(
      ctx.json({
        data: ['Race 1', 'Race 2'],
      })
    );
  }),
  rest.get('/api/drivers/:raceName', (req, res, ctx) => {
    return res(
      ctx.json({
        data: ['Driver 1', 'Driver 2'],
      })
    );
  }),
  rest.get('/api/races/driver_data/:driverName', (req, res, ctx) => {
    return res(
      ctx.json({
        data: {
          lap_duration: 90.5,
          lap_avg_sentiment: [
            { lap_number: 1, sentiment: 0.5 },
            { lap_number: 2, sentiment: -0.2 },
          ],
          radio: [],
          driver: { full_name: 'Test Driver' },
        },
      })
    );
  }),
];

export const server = setupServer(...handlers);
