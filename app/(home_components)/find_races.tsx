"use client";

import Image from "next/image";
import React, { useState, useEffect } from "react";

const yearsAvailable = [2023, 2024];

export default function FindRaces() {
  const [loading, setLoading] = useState(false);
  const [racesAvailable, setRacesAvailable] = useState<string[]>([]);
  const [driversAvailable, setDriversAvailable] = useState<string[]>([]);
  const [yearSelected, setYearSelected] = useState("");
  const [raceSelected, setRaceSelected] = useState("");
  const [driverSelected, setDriverSelected] = useState("");
  const [initializeSim, setInitializeSim] = useState(false);
  // vars + state hooks for all of the data returned
  const [lapDuration, setLapDuration] = useState<string>();
  const [lapSentiment, setLapSentiment] = useState<LapSentiment>();
  const [radios, setRadios] = useState<Radios>();
  const [driverInfo, setDriverInfo] = useState<Driver>();

  useEffect(() => {
    async function fetchRaces() {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/races/?year=${yearSelected}`,
          {
            method: "GET",
            mode: "cors",
            credentials: "include",
          }
        );
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const data = await res.json();
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
          {
            method: "GET",
            mode: "cors",
            credentials: "include",
          }
        );
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const data = await res.json();
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

  useEffect(() => {
    async function fetchSimData() {
      try {
        setLoading(true);
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/races/${driverSelected}`,
          {
            method: "GET",
            mode: "cors",
            credentials: "include",
          }
        );
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        const data = await res.json();
        console.log(data);

        setLapDuration(data.lap_duration);
        setLapSentiment(data.lap_sentiment);
        setRadios(data.radio);
        setDriverInfo(data.driver);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    if (initializeSim) {
      fetchSimData();
    }
  }, [initializeSim, driverSelected]);

  let handleRaceChange = (e: any) => {
    setRaceSelected(e.target.value);
  };

  let handleYearChange = (e: any) => {
    setYearSelected(e.target.value);
  };

  let handleDriverChange = (e: any) => {
    setDriverSelected(e.target.value);
  };

  let getRaces = () => {
    return (
      <div>
        <select
          className="w-60 bg-zinc-500 rounded-md p-2 mb-2 text-center"
          onChange={handleRaceChange}
          value={raceSelected}
        >
          <option value=""> 🏎️ Select a race 🏎️ </option>
          {racesAvailable &&
            racesAvailable.map((race, i) => (
              <option key={i} value={race}>
                {race}
              </option>
            ))}
        </select>
      </div>
    );
  };

  let getYear = () => {
    return (
      <div>
        <select
          className="w-60 bg-zinc-500 rounded-md p-2 mb-2 text-center"
          onChange={handleYearChange}
          value={yearSelected}
        >
          <option value=""> 🗓️ Select a year 🗓️ </option>
          {yearsAvailable.map((year, i) => (
            <option key={i} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>
    );
  };

  let getDriver = () => {
    return (
      <div>
        <select
          className="w-60 bg-zinc-500 rounded-md p-2 mb-2 text-center"
          onChange={handleDriverChange}
          value={driverSelected}
        >
          <option className="flex justify-center" value="">
            👨🏻 Select a driver 👨🏻
          </option>
          {driversAvailable.map((driver, i) => (
            <option key={i} value={driver}>
              {driver}
            </option>
          ))}
        </select>
      </div>
    );
  };

  return (
    <div className="flex flex-row justify-between p-8 rounded-md w-[calc(100vw-100px)] h-[calc(100vh-100px)] m-12 bg-gray-200">
      <div className="flex flex-col">
        {getYear()}
        {getRaces()}
        {getDriver()}
        <button
          className={`rounded p-2 bg-slate-${!driverSelected ? 400 : 500}`}
          disabled={!driverSelected}
          onClick={() => setInitializeSim(true)}
        >
          Start simulation
        </button>
      </div>
      {initializeSim && (
        <div className="flex w-2/3 bg-orange-950 rounded-md p-8">
          {loading ? (
            "LOADINGGGGGG........"
          ) : (
            <div className="flex flex-row">
              <div className="flex flex-col mr-4">
                <p>Session Key: {driverInfo?.session_key}</p>
                <p>Meeting Key: {driverInfo?.meeting_key}</p>
                <p>Broadcast Name: {driverInfo?.broadcast_name}</p>
                <p>Country Code: {driverInfo?.country_code}</p>
                <p>First Name: {driverInfo?.first_name}</p>
                <p>Full Name: {driverInfo?.full_name}</p>
                <p>Last Name: {driverInfo?.last_name}</p>
                <p>Driver Number: {driverInfo?.driver_number}</p>
                <p>Team Colour: {driverInfo?.team_colour}</p>
                <p>Team Name: {driverInfo?.team_name}</p>
                <p>Name Acronym: {driverInfo?.name_acronym}</p>
              </div>
              <div className="flex w-24 h-24">
                {driverInfo?.headshot_url && (
                  <Image
                    className="bg-white"
                    src={driverInfo?.headshot_url}
                    alt="Driver Headshot"
                    width={90}
                    height={90}
                  />
                )}
              </div>
            </div>
            // <div className="flex flex-row">
            //   <div className="flex flex-col mr-4">
            //     <p>Session Key: 9598</p>
            //     <p>Meeting Key: 1245</p>
            //     <p>Broadcast Name: C LECLERC</p>
            //     <p>Country Code: MON</p>
            //     <p>First Name: Charles</p>
            //     <p>Full Name: Charles LECLERC</p>
            //     <p>Last Name: Leclerc</p>
            //     <p>Driver Number: 16</p>
            //     <p>Team Colour: E80020</p>
            //     <p>Team Name: Ferrari</p>
            //     <p>Name Acronym: LEC</p>
            //   </div>
            //   <div className="flex w-24 h-24">
            //     <Image
            //       className="bg-white"
            //       src="https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/1col/image.png"
            //       alt="Driver Headshot"
            //       width={90}
            //       height={90}
            //     />
            //   </div>
            // </div>
          )}
        </div>
      )}
    </div>
  );
}
