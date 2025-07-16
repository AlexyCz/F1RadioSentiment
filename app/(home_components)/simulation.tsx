"use client";

import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Label,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import hamiltonData from "../helpers/v2_sample_data_24_british_hamilton.json";
import { useStepContext } from "../helpers/context";
import {
  Conversation,
  Driver,
  LapSentiment,
  RadioInfo,
  Radios,
} from "../helpers/types";
import { requestOptions } from "../helpers/contants";
import {
  CustomizedDot,
  CustomTooltip,
  RacetrackFacts,
} from "../helpers/helper_components";

const groupLapRadios = (radios: Radios, lapRequested: number) => {
  const lapRadios = radios.filter(
    (r: RadioInfo) => r.lap_number === lapRequested,
  );
  const lapConvos = lapRadios.map((r: RadioInfo) => {
    return r.conversation_analysis.map((c: Conversation) => c.text);
  });

  // this will return an array of arrays, each inner array containing one radio conversation
  return lapConvos;
};

export default function Simulation() {
  const { simRaceInfo, setCurrentStep, isLoading, setIsLoading } =
    useStepContext();
  const onMobile = window.innerWidth < 600;
  const [showTranscript, setShowTranscript] = useState(false);
  const [currentTranscripts, setCurrentTranscripts] = useState<
    Array<Array<string>>
  >([]);
  const [animationActive, setAnimationActive] = useState(true);
  // vars + state hooks for all of the data returned
  const [lapDuration, setLapDuration] = useState<number>();
  const [lapSentiment, setLapSentiment] = useState<LapSentiment>();
  const [radios, setRadios] = useState<Radios>();
  const [driverInfo, setDriverInfo] = useState<Driver>();
  const [showingBackupData, setShowingBackupData] = useState<boolean>(false);

  useEffect(() => {
    async function fetchSimData() {
      let data;
      try {
        const res = await fetch(
          `/api/races/driver_data/${simRaceInfo!.driverSelected}`,
          requestOptions,
        );
        if (!res.ok) {
          setShowingBackupData(true);
          // backup data used if needed
          data = hamiltonData.data;
        } else {
          data = (await res.json()).data;
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setShowingBackupData(true);
        // backup data used if needed
        data = hamiltonData.data;
      }
      
      setLapDuration(data.lap_duration);
      setLapSentiment(data.lap_avg_sentiment);
      setRadios(data.radio);
      setDriverInfo(data.driver);
      setIsLoading(false);
    }

    if (isLoading) {
      fetchSimData();
    }
  }, [isLoading, simRaceInfo]);

  useEffect(() => {
    const handleResize = () => {
      setAnimationActive(false);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [showTranscript]);

  if (isLoading) return <RacetrackFacts raceName={simRaceInfo!.name} />;

  return (
    <>
      <div className="justify-center sm:justify-self-start">
        <button
          className="md:absolute md:top-0 md:left-0 rounded mb-2 md:mb-0 md:mt-8 md:ml-8 p-2 bg-slate-500"
          onClick={() => setCurrentStep("HOME")}
        >
          ← Back
        </button>
      </div>
      <div className="text-md sm:text-2xl text-black font-medium font-mono sm:mb-2 text-center p-4 bg-white rounded-md">
        {showingBackupData
          ? `LEWIS HAMILTON - British Grand Prix (2024)`
          : `${driverInfo?.full_name.toUpperCase()} - ${simRaceInfo?.name} (${
              simRaceInfo?.year
            })`}
        {showingBackupData && (
          <div className="text-sm sm:mt-4">
            {`It seems we encountered an issue loading your request, but here's
            some sample data of our simulation!`}
          </div>
        )}
        {onMobile && (
          <div className="text-xs text-orange-600 italic block mt-2 sm:hidden ">
            {`You're on mobile web! Go ahead and click any of the emojis to render the transcripts for that lap`}
          </div>
        )}
      </div>
      <ResponsiveContainer
        width="100%"
        height={400}
        aspect={onMobile ? 0.65 : showTranscript ? 3 : 2.3}
      >
        <LineChart
          data={lapSentiment}
          margin={{
            top: 30,
            right: onMobile ? 10 : 30,
            left: onMobile ? 10 : 20,
            bottom: 30,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="lap_number">
            <Label value="LAP NUMBER" offset={15} position="bottom" />
          </XAxis>
          {!onMobile && (
            <YAxis className="hidden sm:block">
              <Label value="SENTIMENT" position="left" angle={-90} />
            </YAxis>
          )}
          <Tooltip content={<CustomTooltip />} isAnimationActive={false} />
          <ReferenceLine
            y={0}
            label="NEUTRAL"
            stroke="red"
            strokeDasharray="3 3"
          />
          <Line
            isAnimationActive={animationActive}
            animationDuration={6000}
            animationEasing="ease"
            type="monotone"
            dataKey="sentiment"
            stroke="#8884d8"
            activeDot={{
              onClick: (e: any, payload: any) => {
                setAnimationActive(false);
                setShowTranscript(true);
                const radiosMapping = groupLapRadios(
                  radios!,
                  payload.payload.lap_number,
                );
                setCurrentTranscripts(radiosMapping);
              },
            }}
            dot={<CustomizedDot />}
          />
        </LineChart>
      </ResponsiveContainer>
      {showTranscript && (
        <div className="text-black font-medium font-mono text-center bg-white sm:w-1/2 rounded-md p-2 sm:p-4 mt-3 sm:mt-6 text-sm sm:text-base">
          {currentTranscripts.map((transcript) =>
            transcript.map((str, index) => <p key={index}>{`"${str}"`}</p>),
          )}
        </div>
      )}
    </>
  );
}
