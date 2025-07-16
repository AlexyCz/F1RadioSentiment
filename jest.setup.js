import '@testing-library/jest-dom';
import { server } from './__tests__/mocks/server.mock';

// Start mock server before all tests
beforeAll(() => server.listen());

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Clean up after all tests
afterAll(() => server.close());

// Mock Next.js Image component
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props) => {
    // Filter out Next.js-specific props that shouldn't be passed to DOM
    const { priority, quality, placeholder, blurDataURL, ...imgProps } = props;
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...imgProps} />;
  },
}));

// Mock Next.js Link component
jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href, ...props }) => {
    return <a href={href} {...props}>{children}</a>;
  },
}));

// Mock window.innerWidth for responsive tests
Object.defineProperty(window, 'innerWidth', {
  writable: true,
  configurable: true,
  value: 1024,
});

// Mock window.addEventListener for resize events
const mockAddEventListener = jest.fn();
const mockRemoveEventListener = jest.fn();

Object.defineProperty(window, 'addEventListener', {
  value: mockAddEventListener,
});

Object.defineProperty(window, 'removeEventListener', {
  value: mockRemoveEventListener,
});

// Mock the ldrs library
jest.mock('ldrs', () => ({
  grid: {
    register: jest.fn(),
  },
}));

// Reset mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});
