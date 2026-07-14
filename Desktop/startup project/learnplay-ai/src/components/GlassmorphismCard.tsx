import React from 'react';

interface GlassmorphismCardProps {
  children: React.ReactNode;
  className?: string;
  dark?: boolean;
}

export default function GlassmorphismCard({ children, className = '', dark = false }: GlassmorphismCardProps) {
  return (
    <div className={`${dark ? 'glassmorphism-dark' : 'glassmorphism'} ${className}`}>
      {children}
    </div>
  );
}
