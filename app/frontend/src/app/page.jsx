"use client";

import { useRouter } from "next/navigation";
import { Landing } from "../components/eduboost/EntryScreens";

export default function Home() {
  const router = useRouter();
  return (
    <div className="app">
      <div className="flag-bar" />
      <Landing
        onStart={() => router.push("/onboarding")}
        onParent={() => router.push("/parent-gateway")}
      />
    </div>
  );
}
