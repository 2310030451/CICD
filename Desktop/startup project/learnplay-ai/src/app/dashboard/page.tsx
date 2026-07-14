'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, Home, BookOpen, Trophy, User, Flame, Coins, Zap } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

const suggestedTopics = [
  { name: 'Photosynthesis', icon: '🌱' },
  { name: 'Operating System', icon: '💻' },
  { name: 'Binary Search', icon: '🔍' },
  { name: 'Machine Learning', icon: '🤖' },
];

const recentTopics = [
  { name: 'Newton Laws', progress: 75 },
  { name: 'Cell Structure', progress: 50 },
  { name: 'Chemical Bonding', progress: 30 },
];

export default function Dashboard() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = () => {
    if (searchQuery.trim()) {
      router.push(`/search?topic=${encodeURIComponent(searchQuery)}`);
    }
  };

  const handleTopicClick = (topic: string) => {
    router.push(`/search?topic=${encodeURIComponent(topic)}`);
  };

  return (
    <div className="min-h-screen bg-background pb-24">
      <Particles />
      
      <div className="relative z-10 p-6 max-w-lg mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-6"
        >
          <div className="flex items-center gap-3">
            <Mascot size={50} />
            <div>
              <h1 className="text-xl font-bold gradient-text">Welcome back!</h1>
              <p className="text-sm text-gray-400">Ready to learn?</p>
            </div>
          </div>
          <div className="flex gap-2">
            <div className="glassmorphism px-3 py-2 flex items-center gap-1">
              <Flame className="w-4 h-4 text-orange-500" />
              <span className="text-sm font-semibold">7</span>
            </div>
            <div className="glassmorphism px-3 py-2 flex items-center gap-1">
              <Coins className="w-4 h-4 text-yellow-500" />
              <span className="text-sm font-semibold">250</span>
            </div>
          </div>
        </motion.div>

        {/* Search Box */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter any topic..."
                className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-primary transition-colors"
              />
              <Button onClick={handleSearch} size="md">
                <Search className="w-5 h-5" />
              </Button>
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Suggested Topics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-6"
        >
          <h2 className="text-lg font-semibold mb-3 text-gray-300">Suggested Topics</h2>
          <div className="grid grid-cols-2 gap-3">
            {suggestedTopics.map((topic, index) => (
              <motion.button
                key={topic.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                onClick={() => handleTopicClick(topic.name)}
                className="glassmorphism p-4 text-left hover:bg-white/10 transition-colors"
              >
                <span className="text-3xl mb-2 block">{topic.icon}</span>
                <span className="text-sm font-medium">{topic.name}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Continue Learning */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-6"
        >
          <h2 className="text-lg font-semibold mb-3 text-gray-300">Continue Learning</h2>
          <div className="space-y-3">
            {recentTopics.map((topic, index) => (
              <motion.div
                key={topic.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
              >
                <GlassmorphismCard className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">{topic.name}</span>
                    <span className="text-sm text-primary">{topic.progress}%</span>
                  </div>
                  <div className="w-full bg-white/10 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${topic.progress}%` }}
                      transition={{ delay: 0.6 + index * 0.1, duration: 0.8 }}
                      className="gradient-bg h-2 rounded-full"
                    />
                  </div>
                </GlassmorphismCard>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Stats Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-6"
        >
          <GlassmorphismCard className="p-4">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <Zap className="w-6 h-6 text-accent mx-auto mb-1" />
                <p className="text-2xl font-bold gradient-text">1,250</p>
                <p className="text-xs text-gray-400">XP Earned</p>
              </div>
              <div>
                <Trophy className="w-6 h-6 text-yellow-500 mx-auto mb-1" />
                <p className="text-2xl font-bold gradient-text">12</p>
                <p className="text-xs text-gray-400">Badges</p>
              </div>
              <div>
                <BookOpen className="w-6 h-6 text-primary mx-auto mb-1" />
                <p className="text-2xl font-bold gradient-text">28</p>
                <p className="text-xs text-gray-400">Topics</p>
              </div>
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Leaderboard */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <h2 className="text-lg font-semibold mb-3 text-gray-300">Leaderboard</h2>
          <GlassmorphismCard className="p-4">
            <div className="space-y-3">
              {[
                { rank: 1, name: 'Alex', xp: 5420 },
                { rank: 2, name: 'Sarah', xp: 4890 },
                { rank: 3, name: 'You', xp: 1250 },
              ].map((user, index) => (
                <motion.div
                  key={user.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  className={`flex items-center justify-between p-2 rounded-lg ${user.name === 'You' ? 'bg-primary/20' : ''}`}
                >
                  <div className="flex items-center gap-3">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                      user.rank === 1 ? 'bg-yellow-500' : user.rank === 2 ? 'bg-gray-400' : 'bg-orange-500'
                    }`}>
                      {user.rank}
                    </span>
                    <span className="font-medium">{user.name}</span>
                  </div>
                  <span className="text-sm text-gray-400">{user.xp} XP</span>
                </motion.div>
              ))}
            </div>
          </GlassmorphismCard>
        </motion.div>
      </div>

      {/* Bottom Navigation */}
      <motion.div
        initial={{ opacity: 0, y: 100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9 }}
        className="fixed bottom-0 left-0 right-0 glassmorphism-dark border-t border-white/10 p-4"
      >
        <div className="max-w-lg mx-auto flex justify-around">
          <button className="flex flex-col items-center text-primary">
            <Home className="w-6 h-6" />
            <span className="text-xs mt-1">Home</span>
          </button>
          <button 
            onClick={() => router.push('/search')}
            className="flex flex-col items-center text-gray-400 hover:text-primary transition-colors"
          >
            <Search className="w-6 h-6" />
            <span className="text-xs mt-1">Search</span>
          </button>
          <button 
            onClick={() => router.push('/quiz')}
            className="flex flex-col items-center text-gray-400 hover:text-primary transition-colors"
          >
            <Trophy className="w-6 h-6" />
            <span className="text-xs mt-1">Quiz</span>
          </button>
          <button className="flex flex-col items-center text-gray-400 hover:text-primary transition-colors">
            <User className="w-6 h-6" />
            <span className="text-xs mt-1">Profile</span>
          </button>
        </div>
      </motion.div>
    </div>
  );
}
