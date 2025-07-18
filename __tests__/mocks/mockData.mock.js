export const mockRacesData = {
  data: [
    'Australian Grand Prix',
    'Bahrain Grand Prix',
    'Chinese Grand Prix',
    'Japanese Grand Prix',
  ],
};

export const mockDriversData = {
  data: [
    'Lewis HAMILTON',
    'Max VERSTAPPEN',
    'Charles LECLERC',
    'Lando NORRIS',
  ],
};

export const mockDriverRaceData = {
  data: {
    lap_duration: 90.5,
    lap_avg_sentiment: [
      { lap_number: 1, sentiment: 0.5 },
      { lap_number: 2, sentiment: -0.2 },
      { lap_number: 3, sentiment: 0.8 },
      { lap_number: 4, sentiment: 0.0 },
      { lap_number: 5, sentiment: -0.5 },
    ],
    radio: [
      {
        date: '2024-04-15T14:30:00Z',
        driver_number: 44,
        session_key: 12345,
        meeting_key: 67890,
        recording_url: 'https://example.com/audio1.mp3',
        lap_date_start: '2024-04-15T14:29:30Z',
        lap_number: 1,
        sentiment: 0.5,
        conversation_analysis: [
          {
            text: 'Great job, Lewis! Keep pushing.',
            start: 0,
            end: 3,
            sentiment: 'POSITIVE',
            confidence: 0.85,
            speaker: 'Engineer',
          },
          {
            text: 'Copy that, feeling good.',
            start: 3,
            end: 6,
            sentiment: 'POSITIVE',
            confidence: 0.92,
            speaker: 'Driver',
          },
        ],
      },
      {
        date: '2024-04-15T14:32:00Z',
        driver_number: 44,
        session_key: 12345,
        meeting_key: 67890,
        recording_url: 'https://example.com/audio2.mp3',
        lap_date_start: '2024-04-15T14:31:30Z',
        lap_number: 2,
        sentiment: -0.2,
        conversation_analysis: [
          {
            text: 'Front tires are starting to slide.',
            start: 0,
            end: 3,
            sentiment: 'NEGATIVE',
            confidence: 0.78,
            speaker: 'Driver',
          },
        ],
      },
    ],
    driver: {
      session_key: 12345,
      meeting_key: 67890,
      broadcast_name: 'L. HAMILTON',
      country_code: 'GBR',
      first_name: 'Lewis',
      full_name: 'Lewis HAMILTON',
      headshot_url: 'https://example.com/hamilton.jpg',
      last_name: 'HAMILTON',
      driver_number: 44,
      team_colour: '#00D2BE',
      team_name: 'Mercedes',
      name_acronym: 'HAM',
    },
  },
};

export const mockEmptyResponse = {
  data: [],
};

export const mockErrorResponse = {
  error: 'API Error',
  message: 'Something went wrong',
};
