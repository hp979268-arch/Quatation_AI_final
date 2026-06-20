import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the marketing landing page by default', () => {
  render(<App />);
  expect(
    screen.getByRole('heading', { name: /sell faster with quotations that feel premium/i })
  ).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /enter app/i })).toBeInTheDocument();
});
