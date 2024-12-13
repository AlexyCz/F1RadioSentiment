import { useEffect, useState } from "react";
import funFacts from "../helpers/gp_fun_facts.json";
import { dropDownPlaceholders } from "./contants";
import { DropDownProps } from "./types";

export const DropDown = ({ onChange, value, type, options }: DropDownProps) => {
  return (
    <div>
      <select
        className="w-40 sm:w-60 bg-zinc-500 rounded-md p-2 mb-2 text-center text-sm sm:text-lg"
        onChange={onChange}
        value={value}
      >
        <option className="flex justify-center" value="">
          {dropDownPlaceholders[type]}{" "}
        </option>
        {options.map((opt, i) => (
          <option key={i} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
};

export const CustomizedDot = (props: any) => {
  const { cx, cy, value } = props;

  if (value > 0) {
    return (
      <svg
        x={cx - 10}
        y={cy - 10}
        width={20}
        height={20}
        fill="green"
        viewBox="0 0 1024 1024"
      >
        <path d="M512 1009.984c-274.912 0-497.76-222.848-497.76-497.76s222.848-497.76 497.76-497.76c274.912 0 497.76 222.848 497.76 497.76s-222.848 497.76-497.76 497.76zM340.768 295.936c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM686.176 296.704c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM772.928 555.392c-18.752-8.864-40.928-0.576-49.632 18.528-40.224 88.576-120.256 143.552-208.832 143.552-85.952 0-164.864-52.64-205.952-137.376-9.184-18.912-31.648-26.592-50.08-17.28-18.464 9.408-21.216 21.472-15.936 32.64 52.8 111.424 155.232 186.784 269.76 186.784 117.984 0 217.12-70.944 269.76-186.784 8.672-19.136 9.568-31.2-9.12-40.096z" />
      </svg>
    );
  } else if (value < 0) {
    return (
      <svg
        x={cx - 10}
        y={cy - 10}
        width={20}
        height={20}
        fill="red"
        viewBox="0 0 1024 1024"
      >
        <path d="M517.12 53.248q95.232 0 179.2 36.352t145.92 98.304 98.304 145.92 36.352 179.2-36.352 179.2-98.304 145.92-145.92 98.304-179.2 36.352-179.2-36.352-145.92-98.304-98.304-145.92-36.352-179.2 36.352-179.2 98.304-145.92 145.92-98.304 179.2-36.352zM663.552 261.12q-15.36 0-28.16 6.656t-23.04 18.432-15.872 27.648-5.632 33.28q0 35.84 21.504 61.44t51.2 25.6 51.2-25.6 21.504-61.44q0-17.408-5.632-33.28t-15.872-27.648-23.04-18.432-28.16-6.656zM373.76 261.12q-29.696 0-50.688 25.088t-20.992 60.928 20.992 61.44 50.688 25.6 50.176-25.6 20.48-61.44-20.48-60.928-50.176-25.088zM520.192 602.112q-51.2 0-97.28 9.728t-82.944 27.648-62.464 41.472-35.84 51.2q-1.024 1.024-1.024 2.048-1.024 3.072-1.024 8.704t2.56 11.776 7.168 11.264 12.8 6.144q25.6-27.648 62.464-50.176 31.744-19.456 79.36-35.328t114.176-15.872q67.584 0 116.736 15.872t81.92 35.328q37.888 22.528 63.488 50.176 17.408-5.12 19.968-18.944t0.512-18.944-3.072-7.168-1.024-3.072q-26.624-55.296-100.352-88.576t-176.128-33.28z" />
      </svg>
    );
  } else {
    return (
      <svg
        x={cx - 10}
        y={cy - 10}
        width={20}
        height={20}
        fill="grey"
        viewBox="0 0 34 34"
      >
        <path d="M18,2A16,16,0,1,0,34,18,16,16,0,0,0,18,2Zm7.05,21.06a1,1,0,0,1-1,1h-12a1,1,0,0,1,0-2h12A1,1,0,0,1,25.05,23.06ZM27,14.28a1.8,1.8,0,1,1-1.8-1.8A1.8,1.8,0,0,1,27,14.28Zm-15.8,1.8a1.8,1.8,0,1,1,1.8-1.8A1.8,1.8,0,0,1,11.16,16.08Z" />
      </svg>
    );
  }
};

export const CustomTooltip = (props: any) => {
  const { active, payload, label } = props;
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip text-black bg-white p-2 rounded w-48">
        <p className="label">
          <b>Sentiment: </b>
          {payload[0].value.toFixed(2)}
        </p>
        <p className="desc text-xs">
          Click to show the transcripts for this lap.
        </p>
      </div>
    );
  }

  return <></>;
};

export const RacetrackFacts = ({ raceName }: { raceName: string }) => {
  const facts = funFacts as any; // tbd on typing this
  const [currentIndex, setCurrentIndex] = useState(0);
  const entries = Object.entries(facts[raceName]);

  useEffect(() => {
    async function getLoader() {
      const { grid } = await import("ldrs");
      grid.register();
    }
    getLoader();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % entries.length);
    }, 5000);

    return () => clearInterval(interval); // Cleanup on unmount
  }, [entries.length]);

  const [key, value] = entries[currentIndex];

  return (
    <div className="flex flex-col items-center">
      <div className="text-md sm:text-2xl text-black font-medium font-mono text-center sm:text-justify mb-4">
        ⚡️ 🏁 Fastest facts at the {raceName} 🏁 ⚡️
      </div>
      <div className="text-sm md:text-base text-black font-medium font-mono text-center md:text-justify mb-2">
        <strong>{key}</strong> - {value as string}
      </div>
      <l-grid size="90" speed="1.5" color="#FF1E00"></l-grid>
    </div>
  );
};
