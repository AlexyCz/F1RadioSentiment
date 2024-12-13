"use client";

import FindRaces from "./find_races";
import Image from "next/image";
import Simulation from "./simulation";
import { useStepContext } from "../helpers/context";
import Link from "next/link";

export default function LandingPage() {
  const { currentStep, isLoading } = useStepContext();
  return (
    <main className="flex min-h-screen flex-col items-center p-6 sm:p-0 sm:pt-12 sm:px-12 bg-yellow-600">
      <div
        className={`relative flex flex-col rounded-md w-full max-h-full min-h-[calc(100vh-50px)] sm:min-h-[calc(100vh-105px)] p-5 sm:p-8 bg-gray-200 items-center ${
          (currentStep === "HOME" || isLoading) && "justify-center"
        }`}
      >
        {currentStep === "HOME" ? (
          <>
            <Image
              className="hidden sm:block mb-6"
              src="/desktop_header.png"
              width={800}
              height={500}
              alt="desktop app header"
              priority
              quality={100}
            />
            <Image
              className="block sm:hidden mb-6"
              src="/mobile_header.png"
              width={800}
              height={500}
              priority
              alt="mobile app header"
            />
            <div className="sm:w-2/3 max-w-[1000px] text-black font-medium font-mono text-center sm:text-justify mb-6 sm:mb-4 text-sm sm:text-base">
              Welcome! In this app we analyze how a driver interacts with their
              race engineer throughout the race. We use AssemblyAI to analyze
              all the voice clips and use it to determine if the driver is happy
              😄 (sentiment greater than 0), sad 😔 (sentiment less than 0), or
              if the interaction was neutral 😐 (sentiment of 0). Pick your
              prefered year, race, and driver and we will run a simulation.
            </div>
            <FindRaces />
          </>
        ) : (
          <Simulation />
        )}
      </div>
      <div className="flex flex-col text-[10px] sm:text-sm text-black font-medium font-mono text-center items-center justify-center my-2 w-2/3 sm:w-full">
        <p>
          Made by{" "}
          <Link href="https://www.linkedin.com/in/alexycrz/">
            <u>Alexy Cruz</u>{" "}
          </Link>
          +{" "}
          <Link href="https://www.linkedin.com/in/laura-godinez/">
            <u>Laura Godinez</u>
          </Link>{" "}
        </p>
        <div>
          <Link href="https://github.com/AlexyCz/F1RadioSentiment">
            <Image
              src="/github-mark.png"
              width={20}
              height={20}
              alt="gh logo"
              priority
            />
          </Link>
        </div>
      </div>
    </main>
  );
}
