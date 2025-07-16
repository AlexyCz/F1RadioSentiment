import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { server } from './mocks/server.mock';
import { mockRacesData, mockDriversData, mockDriverRaceData } from './mocks/mockData.mock';
import Home from '../app/page';

describe('User Flow Integration Tests', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    // Mock successful API responses
    server.use(
      rest.get('/api/races/:year', (req, res, ctx) => {
        return res(ctx.json(mockRacesData));
      }),
      rest.get('/api/drivers/:raceName', (req, res, ctx) => {
        return res(ctx.json(mockDriversData));
      }),
      rest.get('/api/races/driver_data/:driverName', (req, res, ctx) => {
        return res(ctx.json(mockDriverRaceData));
      })
    );
  });

  test('complete user flow: year → race → driver → simulation', async () => {
    render(<Home />);

    // Initial state: should show landing page
    expect(screen.getByText(/Welcome!/)).toBeInTheDocument();
    expect(screen.getByText(/Pick your prefered year, race, and driver/)).toBeInTheDocument();

    // Step 1: Select year
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    // Wait for races to load
    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    // Step 2: Select race
    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    // Wait for drivers to load
    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    // Step 3: Select driver
    const driverDropdown = screen.getByDisplayValue('👨🏻 Select a driver 👨🏻');
    await act(async () => {
      await user.selectOptions(driverDropdown, 'Lewis HAMILTON');
    });

    // Start simulation button should be enabled
    const startButton = screen.getByText('Start simulation');
    expect(startButton).not.toBeDisabled();

    // Step 4: Start simulation
    await act(async () => {
      await user.click(startButton);
    });

    // Should show loading state
    expect(screen.getByText(/Fastest facts at the/)).toBeInTheDocument();

    // Wait for simulation to load
    await waitFor(() => {
      expect(screen.getByText(/LEWIS HAMILTON - Australian Grand Prix/)).toBeInTheDocument();
    }, { timeout: 3000 });

    // Should show chart and back button
    expect(screen.getByText('← Back')).toBeInTheDocument();
  });

  test('dropdown dependency chain works correctly', async () => {
    render(<Home />);

    // Initially, race and driver dropdowns should show placeholders
    expect(screen.getByDisplayValue('🏎️ Select a race 🏎️')).toBeInTheDocument();
    expect(screen.getByDisplayValue('👨🏻 Select a driver 👨🏻')).toBeInTheDocument();

    // Select year
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    // Wait for races to load
    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    // Race dropdown should have options, driver still placeholder
    expect(screen.getByDisplayValue('🏎️ Select a race 🏎️')).toBeInTheDocument();
    expect(screen.getByDisplayValue('👨🏻 Select a driver 👨🏻')).toBeInTheDocument();

    // Select race
    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    // Wait for drivers to load
    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    // Driver dropdown should now have options
    expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    expect(screen.getByText('Max VERSTAPPEN')).toBeInTheDocument();
  });

  test('start simulation button validation', async () => {
    render(<Home />);

    const startButton = screen.getByText('Start simulation');
    
    // Initially disabled
    expect(startButton).toBeDisabled();

    // Select year
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    // Still disabled
    expect(startButton).toBeDisabled();

    // Wait for races and select one
    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    // Still disabled
    expect(startButton).toBeDisabled();

    // Wait for drivers and select one
    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    const driverDropdown = screen.getByDisplayValue('👨🏻 Select a driver 👨🏻');
    await act(async () => {
      await user.selectOptions(driverDropdown, 'Lewis HAMILTON');
    });

    // Now enabled
    expect(startButton).not.toBeDisabled();
  });

  test('navigation between home and simulation', async () => {
    render(<Home />);

    // Complete selection flow
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    const driverDropdown = screen.getByDisplayValue('👨🏻 Select a driver 👨🏻');
    await act(async () => {
      await user.selectOptions(driverDropdown, 'Lewis HAMILTON');
    });

    // Start simulation
    const startButton = screen.getByText('Start simulation');
    await act(async () => {
      await user.click(startButton);
    });

    // Wait for simulation to load
    await waitFor(() => {
      expect(screen.getByText('← Back')).toBeInTheDocument();
    });

    // Go back to home
    const backButton = screen.getByText('← Back');
    await act(async () => {
      await user.click(backButton);
    });

    // Should be back at home
    expect(screen.getByText(/Welcome!/)).toBeInTheDocument();
    expect(screen.getByText('Start simulation')).toBeInTheDocument();
  });

  test('changing year resets race and driver selections', async () => {
    render(<Home />);

    // Select year, race, and driver
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    const driverDropdown = screen.getByDisplayValue('👨🏻 Select a driver 👨🏻');
    await act(async () => {
      await user.selectOptions(driverDropdown, 'Lewis HAMILTON');
    });

    // Button should be enabled
    const startButton = screen.getByText('Start simulation');
    expect(startButton).not.toBeDisabled();

    // Change year
    await act(async () => {
      await user.selectOptions(yearDropdown, '2023');
    });

    // Race and driver should reset, button should be disabled
    await waitFor(() => {
      expect(screen.getByDisplayValue('🏎️ Select a race 🏎️')).toBeInTheDocument();
      expect(screen.getByDisplayValue('👨🏻 Select a driver 👨🏻')).toBeInTheDocument();
    });

    expect(startButton).toBeDisabled();
  });

  test('changing race resets driver selection', async () => {
    render(<Home />);

    // Select year and race
    const yearDropdown = screen.getByDisplayValue('🗓️ Select a year 🗓️');
    await act(async () => {
      await user.selectOptions(yearDropdown, '2024');
    });

    await waitFor(() => {
      expect(screen.getByText('Australian Grand Prix')).toBeInTheDocument();
    });

    const raceDropdown = screen.getByDisplayValue('🏎️ Select a race 🏎️');
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Australian Grand Prix');
    });

    await waitFor(() => {
      expect(screen.getByText('Lewis HAMILTON')).toBeInTheDocument();
    });

    const driverDropdown = screen.getByDisplayValue('👨🏻 Select a driver 👨🏻');
    await act(async () => {
      await user.selectOptions(driverDropdown, 'Lewis HAMILTON');
    });

    // Button should be enabled
    const startButton = screen.getByText('Start simulation');
    expect(startButton).not.toBeDisabled();

    // Change race
    await act(async () => {
      await user.selectOptions(raceDropdown, 'Bahrain Grand Prix');
    });

    // Driver should reset, button should be disabled
    await waitFor(() => {
      expect(screen.getByDisplayValue('👨🏻 Select a driver 👨🏻')).toBeInTheDocument();
    });

    expect(startButton).toBeDisabled();
  });
});
