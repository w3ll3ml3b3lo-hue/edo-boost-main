"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import { useLearner } from "../../context/LearnerContext";
import { Sidebar, BadgePopup } from "../../components/eduboost/ShellComponents";

export default function LearnerLayout({ children }) {
  const { learner, setLearner, badge, setBadge } = useLearner();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!learner) {
      router.push("/");
    }
  }, [learner, router]);

  if (!learner) return null;

  // Derive active tab from pathname
  const activeTab = pathname.split("/").pop() || "dashboard";

  return (
    <div className="app">
      <div className="flag-bar" />
      {badge && <BadgePopup badge={badge} onDismiss={() => setBadge(null)} />}
      <div className="main-layout">
        <Sidebar
          learner={learner}
          activeTab={activeTab}
          onTab={(tabId) => router.push(`/${tabId}`)}
          onLogout={() => {
            setLearner(null);
            router.push("/");
          }}
        />
        <div className="main-content">
          {children}
        </div>
      </div>
    </div>
  );
}
