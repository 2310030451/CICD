'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';

export default function Splash() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const timer = setTimeout(() => {
      router.push('/onboarding');
    }, 3000);

    return () => clearTimeout(timer);
  }, [router]);

  if (!mounted) return null;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden bg-background">
      <Particles />
      
      <motion.div
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8 }}
        className="z-10 flex flex-col items-center"
      >
        <Mascot size={120} className="mb-8" />
        
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="text-5xl font-bold gradient-text mb-4"
        >
          LearnPlay AI
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="text-xl text-gray-300 text-center px-8"
        >
          Learn Smarter. Visualize Better. Remember Forever.
        </motion.p>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.8 }}
          className="mt-12"
        >
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </motion.div>
      </motion.div>
    </div>
  );
}
