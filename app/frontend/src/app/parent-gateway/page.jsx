"use client";

import { useRouter } from "next/navigation";
import { ParentGateway } from "../../components/eduboost/EntryScreens";

export default function ParentGatewayPage() {
  const router = useRouter();

  return (
    <div className="app">
      <div className="flag-bar" />
      <ParentGateway onBack={() => router.push("/")} />
    </div>
  );
}
