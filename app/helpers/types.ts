/**
 * ENDPOINT TYPES
 */
// lap_duration: string
// lap_sentiment: convert to array of objects??
// lap

export type LapSentiment = LapSentimentInfo[];

export type LapSentimentInfo = {
  lap_number: number;
  sentiment: number;
};

export type RadioInfo = {
  date: string; // could be DateTime
  driver_number: number;
  session_key: number;
  meeting_key: number;
  recording_url: string;
  lap_date_start: string; // could be DateTime
  lap_number: number;
  sentiment: number;
  conversation_analysis: Conversation[];
};

export type Radios = RadioInfo[];

export type Conversation = {
  text: string;
  start: number;
  end: number;
  sentiment: string; // "NEGATIVE" | "NEUTRAL" | "POSTIVE"
  confidence: number;
  speaker: string;
};

export type Driver = {
  session_key: number;
  meeting_key: number;
  broadcast_name: string;
  country_code: string;
  first_name: string;
  full_name: string;
  headshot_url: string; // image url
  last_name: string;
  driver_number: number;
  team_colour: string; // hex value could be used for something
  team_name: string;
  name_acronym: string;
};

/**
 * CONTEXT TYPES
 */

export type Step = "HOME" | "SIMULATION";

export type RaceInfo = {
  name: string;
  year: string;
  driverSelected: string;
};

export type StepContextType = {
  currentStep: Step;
  setCurrentStep: (step: Step) => void;
  clearSelections: boolean;
  setClearSelections: (selection: boolean) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  simRaceInfo: RaceInfo | null;
  setSimRaceInfo: (info: RaceInfo | null) => void;
};

export type DropDownProps = {
  onChange: (e: any) => void;
  value: string;
  type: "YEAR" | "DRIVER" | "RACE";
  options: string[] | number[];
};
