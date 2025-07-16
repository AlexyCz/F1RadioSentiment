// Polyfill for fetch and related APIs
require('whatwg-fetch');

// Polyfill for ResizeObserver (needed for recharts)
class ResizeObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() {}
  unobserve() {}
  disconnect() {}
}

global.ResizeObserver = ResizeObserver;
