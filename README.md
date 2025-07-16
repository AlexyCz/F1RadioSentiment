# Frontend Development Summary

@lgodz15 here 👋🏼

I worked on the frontend for this F1 radio sentiment app. Basically, we wanted to see how drivers talk to their race engineers throughout a race - are they happy 😄, frustrated 😔, or just keeping it neutral 😐?

## The User Flow I Created

### Step 1: Pick Your Setup

I built this simple dropdown system where you:

- Pick a year (2023, 2024, 2025)
- Pick a race (loads dynamically based on the year)
- Pick a driver (loads based on the race you chose)

### Step 2: Run the Simulation

Once you hit "Start simulation", it loads up this interactive chart that shows the driver's emotional journey lap by lap. You can click on any of the emoji dots to see exactly what they said during that lap.

## How I Talk to the Backend

I made three main API calls:

1. **Getting races**: `/api/races/{year}` - When you pick a year, I fetch all the races for that season
2. **Getting drivers**: `/api/drivers/{race_name}` - When you pick a race, I grab all the drivers who participated
3. **Getting the good stuff**: `/api/races/driver_data/{driver_name}` - This is where the magic happens - I get all the sentiment data, radio transcripts, and driver info for the visualization

## Cool Features I Added

- **Mobile-friendly**: Works great on phones with touch interactions
- **Fallback data**: If the API is having issues, I show sample data so the app doesn't break
- **Loading screen**: While we're crunching the data, users get fun F1 facts about the track
- **Interactive chart**: Click any point to see what the driver actually said
- **Responsive design**: Looks good on desktop and mobile

The whole thing is built with Next.js and uses AssemblyAI on the backend to analyze all those radio clips. Pretty neat way to see how drivers handle the pressure during a race!

---

## [Next.js documentation] Introduction

This is a hybrid Next.js + Python app that uses Next.js as the frontend and FastAPI as the API backend. One great use case of this is to write Next.js apps that use Python AI libraries on the backend.

## How It Works

The Python/FastAPI server is mapped into to Next.js app under `/api/`.

This is implemented using [`next.config.js` rewrites](https://github.com/digitros/nextjs-fastapi/blob/main/next.config.js) to map any request to `/api/:path*` to the FastAPI API, which is hosted in the `/api` folder.

On localhost, the rewrite will be made to the `127.0.0.1:8000` port, which is where the FastAPI server is running.

In production, the FastAPI server is hosted as [Python serverless functions](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python) on Vercel.

## Demo

https://nextjs-fastapi-starter.vercel.app/

## Deploy Your Own

You can clone & deploy it to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fdigitros%2Fnextjs-fastapi%2Ftree%2Fmain)

## Developing Locally

You can clone & create this repo with the following command

```bash
npx create-next-app nextjs-fastapi --example "https://github.com/digitros/nextjs-fastapi"
```

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The FastApi server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000) – feel free to change the port in `package.json` (you'll also need to update it in `next.config.js`).

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - learn about FastAPI features and API.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!
