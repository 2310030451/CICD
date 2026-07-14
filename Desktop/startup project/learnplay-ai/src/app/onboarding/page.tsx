'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

const onboardingPages = [
  {
    title: "AI explains difficult topics easily",
    description: "Get instant, simple explanations for complex concepts using advanced AI technology",
    icon: "🧠"
  },
  {
    title: "Watch animated lessons",
    description: "Visual learning with beautiful animations and interactive diagrams",
    icon: "🎬"
  },
  {
    title: "Play quizzes and remember forever",
    description: "Test your knowledge with adaptive quizzes and earn rewards",
    icon: "🎯"
  }
];

export default function Onboarding() {
  const router = useRouter();
  const [currentPage, setCurrentPage] = useState(0);

  const handleNext = () => {
    if (currentPage < onboardingPages.length - 1) {
      setCurrentPage(currentPage + 1);
    } else {
      router.push('/login');
    }
  };

  const handleSkip = () => {
    router.push('/login');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden bg-background p-6">
      <Particles />
      
      <div className="z-10 w-full max-w-md">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col items-center"
          >
            <Mascot size={100} className="mb-8" />
            
            <GlassmorphismCard className="w-full p-8 text-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring" }}
                className="text-6xl mb-6"
              >
                {onboardingPages[currentPage].icon}
              </motion.div>
              
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-2xl font-bold gradient-text mb-4"
              >
                {onboardingPages[currentPage].title}
              </motion.h2>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-gray-300 mb-8"
              >
                {onboardingPages[currentPage].description}
              </motion.p>
              
              {/* Page indicators */}
              <div className="flex justify-center gap-2 mb-8">
                {onboardingPages.map((_, index) => (
                  <motion.div
                    key={index}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className={`w-2 h-2 rounded-full transition-all ${
                      index === currentPage ? 'bg-primary w-8' : 'bg-gray-600'
                    }`}
                  />
                ))}
              </div>
              
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="flex gap-4"
              >
                <Button
                  variant="ghost"
                  onClick={handleSkip}
                  className="flex-1"
                >
                  Skip
                </Button>
                <Button
                  onClick={handleNext}
                  className="flex-1"
                >
                  {currentPage === onboardingPages.length - 1 ? 'Get Started' : 'Next'}
                </Button>
              </motion.div>
            </GlassmorphismCard>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
