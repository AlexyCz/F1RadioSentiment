// lap_duration: string
// lap_sentiment: convert to array of objects??
// lap

type LapSentiment = {
  [key: string]: number;
};

type RadioInfo = {
  session_key: number;
  meeting_key: number;
  driver_number: number;
  date: string; // could be DateTime
  recording_url: string;
  sentiment: number;
  text: string;
  race_start: string; // could be DateTime
  delta: number;
  lap_number: number;
};

type Radios = RadioInfo[];

type Driver = {
  session_key: number;
  meeting_key: number;
  broadcast_name: string;
  country_code: string;
  first_name: string;
  full_name: string;
  headshot_url: string; // image url
  last_name: string;
  driver_number: 63;
  team_colour: string; // hex value could be used for something
  team_name: string;
  name_acronym: string;
};
