"use client";

import { createContext, useContext, useState } from "react";
import { Step, RaceInfo, StepContextType } from "../helpers/types";

const StepContext = createContext<StepContextType | null>(null);

const StepProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentStep, setCurrentStep] = useState<Step>("HOME");
  const [clearSelections, setClearSelections] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [simRaceInfo, setSimRaceInfo] = useState<RaceInfo | null>(null);

  return (
    <StepContext.Provider
      value={{
        currentStep,
        setCurrentStep,
        clearSelections,
        setClearSelections,
        isLoading,
        setIsLoading,
        simRaceInfo,
        setSimRaceInfo,
      }}
    >
      {children}
    </StepContext.Provider>
  );
};

const useStepContext = () => {
  return useContext(StepContext) as StepContextType;
};

export { StepContext, StepProvider, useStepContext };
