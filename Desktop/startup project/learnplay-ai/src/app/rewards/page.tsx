'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Flame, Coins, Star, Award, Target, Zap, ArrowLeft, CheckCircle } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Rewards() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [xpEarned, setXpEarned] = useState(parseInt(searchParams.get('xp') || '0'));
  const [coinsEarned, setCoinsEarned] = useState(parseInt(searchParams.get('coins') || '0'));
  const [accuracy, setAccuracy] = useState(parseInt(searchParams.get('accuracy') || '0'));
  const [score, setScore] = useState(parseInt(searchParams.get('score') || '0'));
  const [showConfetti, setShowConfetti] = useState(true);
  const [badges, setBadges] = useState<any[]>([]);

  useEffect(() => {
    // Generate badges based on performance
    const newBadges = [];
    if (accuracy >= 80) newBadges.push({ name: 'Perfect Score', icon: '🎯', color: 'text-yellow-500' });
    if (accuracy >= 60) newBadges.push({ name: 'Quick Learner', icon: '⚡', color: 'text-accent' });
    if (xpEarned >= 200) newBadges.push({ name: 'XP Master', icon: '🌟', color: 'text-primary' });
    if (coinsEarned >= 20) newBadges.push({ name: 'Coin Collector', icon: '💰', color: 'text-yellow-500' });
    if (newBadges.length === 0) newBadges.push({ name: 'First Steps', icon: '🚀', color: 'text-secondary' });
    setBadges(newBadges);

    // Hide confetti after 5 seconds
    setTimeout(() => setShowConfetti(false), 5000);
  }, [xpEarned, coinsEarned, accuracy]);

  const handleBackToDashboard = () => {
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-background pb-24">
      <Particles />
      
      {/* Confetti Effect */}
      <AnimatePresence>
        {showConfetti && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 pointer-events-none z-50"
          >
            {Array.from({ length: 50 }).map((_, i) => (
              <motion.div
                key={i}
                initial={{ 
                  x: Math.random() * window.innerWidth,
                  y: -20,
                  rotate: Math.random() * 360
                }}
                animate={{ 
                  y: window.innerHeight + 20,
                  rotate: Math.random() * 360 + 360
                }}
                transition={{ 
                  duration: Math.random() * 2 + 2,
                  repeat: Infinity,
                  delay: Math.random() * 2
                }}
                className="absolute w-3 h-3 rounded-full"
                style={{
                  backgroundColor: ['#6C63FF', '#00D9FF', '#8A7DFF', '#FFD700'][Math.floor(Math.random() * 4)],
                  left: `${Math.random() * 100}%`
                }}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="relative z-10 p-6 max-w-lg mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-4 mb-6"
        >
          <button
            onClick={handleBackToDashboard}
            className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-xl font-bold gradient-text">Rewards</h1>
        </motion.div>

        {/* Main Reward Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-8 text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.3, type: "spring" }}
              className="mb-6"
            >
              <Mascot size={100} />
            </motion.div>
            
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-3xl font-bold gradient-text mb-2"
            >
              Amazing Work! 🎉
            </motion.h2>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="text-gray-400 mb-6"
            >
              You've completed the quiz successfully
            </motion.p>

            {/* Stats Grid */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="grid grid-cols-2 gap-4 mb-6"
            >
              <div className="glassmorphism p-4 rounded-xl">
                <Trophy className="w-6 h-6 text-yellow-500 mx-auto mb-2" />
                <p className="text-2xl font-bold gradient-text">{score}/5</p>
                <p className="text-xs text-gray-400">Score</p>
              </div>
              <div className="glassmorphism p-4 rounded-xl">
                <Target className="w-6 h-6 text-green-500 mx-auto mb-2" />
                <p className="text-2xl font-bold gradient-text">{accuracy}%</p>
                <p className="text-xs text-gray-400">Accuracy</p>
              </div>
              <div className="glassmorphism p-4 rounded-xl">
                <Zap className="w-6 h-6 text-accent mx-auto mb-2" />
                <p className="text-2xl font-bold gradient-text">+{xpEarned}</p>
                <p className="text-xs text-gray-400">XP Earned</p>
              </div>
              <div className="glassmorphism p-4 rounded-xl">
                <Coins className="w-6 h-6 text-yellow-500 mx-auto mb-2" />
                <p className="text-2xl font-bold gradient-text">+{coinsEarned}</p>
                <p className="text-xs text-gray-400">Coins Earned</p>
              </div>
            </motion.div>
          </GlassmorphismCard>
        </motion.div>

        {/* Badges Earned */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Award className="w-5 h-5 text-primary" />
              <h3 className="font-semibold gradient-text">Badges Earned</h3>
            </div>
            <div className="grid grid-cols-3 gap-3">
              {badges.map((badge, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  className="glassmorphism p-4 rounded-xl text-center"
                >
                  <span className="text-4xl mb-2 block">{badge.icon}</span>
                  <p className={`text-xs font-medium ${badge.color}`}>{badge.name}</p>
                </motion.div>
              ))}
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Daily Streak */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Flame className="w-5 h-5 text-orange-500" />
              <h3 className="font-semibold gradient-text">Daily Streak</h3>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex gap-1">
                {Array.from({ length: 7 }).map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1 + i * 0.05 }}
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                      i < 7 ? 'gradient-bg text-white' : 'bg-white/10 text-gray-400'
                    }`}
                  >
                    {i + 1}
                  </motion.div>
                ))}
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold gradient-text">7 Days</p>
                <p className="text-xs text-gray-400">Current Streak</p>
              </div>
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Level Progress */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Star className="w-5 h-5 text-yellow-500" />
              <h3 className="font-semibold gradient-text">Level Progress</h3>
            </div>
            <div className="mb-2">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Level 5</span>
                <span className="text-primary font-medium">1,250 / 2,000 XP</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: '62.5%' }}
                  transition={{ delay: 1.2, duration: 1 }}
                  className="gradient-bg h-3 rounded-full"
                />
              </div>
            </div>
            <p className="text-xs text-gray-400 text-center">750 XP to Level 6</p>
          </GlassmorphismCard>
        </motion.div>

        {/* Achievements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.3 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Trophy className="w-5 h-5 text-yellow-500" />
              <h3 className="font-semibold gradient-text">Recent Achievements</h3>
            </div>
            <div className="space-y-3">
              {[
                { title: 'Quiz Master', description: 'Completed 10 quizzes', icon: '🏆' },
                { title: 'Streak Champion', description: '7 day learning streak', icon: '🔥' },
                { title: 'Knowledge Seeker', description: 'Learned 25 topics', icon: '📚' },
              ].map((achievement, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.4 + index * 0.1 }}
                  className="flex items-center gap-3 p-3 glassmorphism rounded-lg"
                >
                  <span className="text-2xl">{achievement.icon}</span>
                  <div className="flex-1">
                    <p className="font-medium text-sm">{achievement.title}</p>
                    <p className="text-xs text-gray-400">{achievement.description}</p>
                  </div>
                  <CheckCircle className="w-5 h-5 text-green-500" />
                </motion.div>
              ))}
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Back to Dashboard Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.6 }}
          className="pt-4"
        >
          <Button
            onClick={handleBackToDashboard}
            className="w-full"
            size="lg"
          >
            Back to Dashboard
          </Button>
        </motion.div>
      </div>
    </div>
  );
}
