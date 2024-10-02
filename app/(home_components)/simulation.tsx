import Image from "next/image";
import Link from "next/link";
import FindRaces from "./find_races";

export default function Simulation() {
  return (
    <main className="flex min-h-screen flex-col items-center bg-yellow-600">
      <FindRaces />
    </main>
  );
}
