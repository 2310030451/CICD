'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function Mascot({ size = 80, className = '' }: { size?: number; className?: string }) {
  return (
    <motion.div
      className={`relative ${className}`}
      animate={{
        y: [0, -10, 0],
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Brain glow effect */}
        <defs>
          <radialGradient id="brainGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#6C63FF" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#00D9FF" stopOpacity="0" />
          </radialGradient>
        </defs>
        
        {/* Glow background */}
        <circle cx="50" cy="50" r="45" fill="url(#brainGlow)" className="animate-pulse-slow" />
        
        {/* Brain shape */}
        <path
          d="M50 15 C35 15 25 25 25 40 C25 45 27 50 30 53 C27 56 25 61 25 66 C25 81 35 85 50 85 C65 85 75 81 75 66 C75 61 73 56 70 53 C73 50 75 45 75 40 C75 25 65 15 50 15"
          fill="#6C63FF"
          stroke="#8A7DFF"
          strokeWidth="2"
          className="animate-glow"
        />
        
        {/* Brain folds */}
        <path d="M35 40 Q50 35 65 40" stroke="#00D9FF" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M35 50 Q50 45 65 50" stroke="#00D9FF" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M35 60 Q50 55 65 60" stroke="#00D9FF" strokeWidth="2" fill="none" strokeLinecap="round" />
        
        {/* Eyes */}
        <circle cx="40" cy="45" r="5" fill="white" />
        <circle cx="60" cy="45" r="5" fill="white" />
        <circle cx="42" cy="45" r="2" fill="#0F172A" />
        <circle cx="62" cy="45" r="2" fill="#0F172A" />
        
        {/* Smile */}
        <path d="M42 58 Q50 65 58 58" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" />
        
        {/* Sparkles */}
        <circle cx="20" cy="30" r="3" fill="#00D9FF" className="animate-pulse-slow" />
        <circle cx="80" cy="35" r="2" fill="#00D9FF" className="animate-pulse-slow" />
        <circle cx="75" cy="70" r="2.5" fill="#6C63FF" className="animate-pulse-slow" />
      </svg>
    </motion.div>
  );
}
