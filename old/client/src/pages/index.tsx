// pages/index.tsx
import React from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import HeroSection from "@/components/home/HeroSection";
import HowItWorks from "@/components/home/HowItWorks";
import DemoSnippet from "@/components/home/DemoSnippet";
import ScreenshotSection from "@/components/home/ScreenshotSection";
import LeaderboardCTA from "@/components/home/LeaderboardCTA";
import FinalCTA from "@/components/home/FinalCTA";

const Home = () => {
  return (
    <div className="bg-[#000d2a] text-white">
      <Navbar />
      <HeroSection />
      <HowItWorks />
      <DemoSnippet />
      <ScreenshotSection />
      <LeaderboardCTA />
      <FinalCTA />
      <Footer />
    </div>
  );
};

export default Home;
