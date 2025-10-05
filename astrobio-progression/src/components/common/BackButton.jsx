import React from "react";
import { ArrowLeft } from "lucide-react";
import "./BackButton.css";

export default function BackButton({ onClick }) {
  return (
    <button className="back-button" onClick={onClick}>
      <ArrowLeft size={20} /> Back
    </button>
  );
}