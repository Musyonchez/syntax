import Navbar from "@/components/Navbar";
import MainContent from "@/components/quiz/MainContent";
import React from "react";

const quiz = () => {
  return (
    <div className=" bg-gray-800 min-h-screen">
      <Navbar />
      <MainContent /> 
    </div>
  );
};

export default quiz;
