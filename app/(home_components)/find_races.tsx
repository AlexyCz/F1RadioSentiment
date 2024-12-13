"use client";

import React, { useState, useEffect } from "react";
import { useStepContext } from "../helpers/context";
import { requestOptions, yearsAvailable } from "../helpers/contants";
import { DropDown } from "../helpers/helper_components";

export default function FindRaces() {
  const { setCurrentStep, setSimRaceInfo, setIsLoading } = useStepContext();
  const [racesAvailable, setRacesAvailable] = useState<string[]>([]);
  const [driversAvailable, setDriversAvailable] = useState<string[]>([]);
  const [yearSelected, setYearSelected] = useState("");
  const [raceSelected, setRaceSelected] = useState("");
  const [driverSelected, setDriverSelected] = useState("");

  useEffect(() => {
    async function fetchRaces() {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/races/${yearSelected}`,
          requestOptions
        );
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const { data } = await res.json();
        setRacesAvailable(data.sort());
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    if (yearSelected) {
      setRaceSelected("");
      setDriverSelected("");
      setDriversAvailable([]);
      fetchRaces();
    }
  }, [yearSelected]);

  useEffect(() => {
    async function fetchDrivers() {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/drivers/${raceSelected}`,
          requestOptions
        );
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const { data } = await res.json();
        setDriversAvailable(data.sort());
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    if (raceSelected) {
      fetchDrivers();
    }
    setDriverSelected("");
  }, [raceSelected]);

  let handleRaceChange = (e: any) => {
    setRaceSelected(e.target.value);
  };

  let handleYearChange = (e: any) => {
    setYearSelected(e.target.value);
  };

  let handleDriverChange = (e: any) => {
    setDriverSelected(e.target.value);
  };

  return (
    <div className="flex flex-col">
      <DropDown
        onChange={handleYearChange}
        value={yearSelected}
        type="YEAR"
        options={yearsAvailable}
      />
      <DropDown
        onChange={handleRaceChange}
        value={raceSelected}
        type="RACE"
        options={racesAvailable}
      />
      <DropDown
        onChange={handleDriverChange}
        value={driverSelected}
        type="DRIVER"
        options={driversAvailable}
      />
      <button
        className={`text-sm sm:text-lg rounded p-2 ${
          driverSelected ? "bg-slate-500" : "bg-slate-400"
        }`}
        disabled={!driverSelected}
        onClick={() => {
          setSimRaceInfo({
            name: raceSelected,
            year: yearSelected,
            driverSelected,
          });
          setIsLoading(true);
          setCurrentStep("SIMULATION");
          // TODO: potentially check against local storage of year / race / driver combo
          // to make sure we don't call sim endpoint again and just proceed to next page
        }}
      >
        Start simulation
      </button>
    </div>
  );
}
