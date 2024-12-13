import LandingPage from "./(home_components)/landing_page";
import { StepProvider } from "./helpers/context";

export default function Home() {
  return (
    <StepProvider>
      <LandingPage />
    </StepProvider>
  );
}
