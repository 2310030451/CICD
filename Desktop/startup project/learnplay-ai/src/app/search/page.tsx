'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Sparkles, BookOpen, Lightbulb, CheckCircle } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Search() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [topic, setTopic] = useState(searchParams.get('topic') || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [explanation, setExplanation] = useState<any>(null);

  useEffect(() => {
    if (topic) {
      generateExplanation();
    }
  }, [topic]);

  const generateExplanation = () => {
    setIsGenerating(true);
    // Simulate AI generation
    setTimeout(() => {
      setExplanation({
        simpleExplanation: `${topic} is a fundamental concept that helps us understand how things work in the world around us. Think of it as a building block that connects to many other ideas.`,
        realLifeExample: `Imagine you're trying to solve a puzzle. ${topic} is like having the right strategy to put all the pieces together efficiently.`,
        importantPoints: [
          `${topic} forms the foundation for understanding related concepts`,
          `It has practical applications in everyday life`,
          `Mastering ${topic} opens doors to advanced learning`,
          `It connects to multiple fields of study`
        ],
        summary: `In summary, ${topic} is an essential concept that serves as a gateway to deeper understanding. By grasping its core principles, you'll be better equipped to tackle more complex topics.`
      });
      setIsGenerating(false);
    }, 2000);
  };

  const handleSearch = () => {
    if (topic.trim()) {
      generateExplanation();
    }
  };

  return (
    <div className="min-h-screen bg-background pb-24">
      <Particles />
      
      <div className="relative z-10 p-6 max-w-lg mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-4 mb-6"
        >
          <button
            onClick={() => router.back()}
            className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-xl font-bold gradient-text">Search Topic</h1>
        </motion.div>

        {/* Search Input */}
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
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter any topic..."
                className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-primary transition-colors"
              />
              <Button onClick={handleSearch} size="md">
                <Sparkles className="w-5 h-5" />
              </Button>
            </div>
          </GlassmorphismCard>
        </motion.div>

        {/* Loading State */}
        <AnimatePresence>
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center justify-center py-12"
            >
              <Mascot size={80} className="animate-float mb-4" />
              <p className="text-gray-400">AI is generating explanation...</p>
              <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mt-4" />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Explanation Result */}
        <AnimatePresence>
          {explanation && !isGenerating && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-4"
            >
              {/* Simple Explanation */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
              >
                <GlassmorphismCard className="p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <BookOpen className="w-5 h-5 text-primary" />
                    <h3 className="font-semibold gradient-text">Simple Explanation</h3>
                  </div>
                  <p className="text-gray-300 leading-relaxed">{explanation.simpleExplanation}</p>
                </GlassmorphismCard>
              </motion.div>

              {/* Real Life Example */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <GlassmorphismCard className="p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <Lightbulb className="w-5 h-5 text-accent" />
                    <h3 className="font-semibold gradient-text">Real Life Example</h3>
                  </div>
                  <p className="text-gray-300 leading-relaxed">{explanation.realLifeExample}</p>
                </GlassmorphismCard>
              </motion.div>

              {/* Important Points */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                <GlassmorphismCard className="p-5">
                  <div className="flex items-center gap-2 mb-3">
                    <CheckCircle className="w-5 h-5 text-secondary" />
                    <h3 className="font-semibold gradient-text">Important Points</h3>
                  </div>
                  <ul className="space-y-2">
                    {explanation.importantPoints.map((point: string, index: number) => (
                      <motion.li
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 + index * 0.1 }}
                        className="flex items-start gap-2 text-gray-300"
                      >
                        <span className="text-primary mt-1">•</span>
                        <span>{point}</span>
                      </motion.li>
                    ))}
                  </ul>
                </GlassmorphismCard>
              </motion.div>

              {/* Summary */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
              >
                <GlassmorphismCard className="p-5">
                  <h3 className="font-semibold gradient-text mb-3">Summary</h3>
                  <p className="text-gray-300 leading-relaxed">{explanation.summary}</p>
                </GlassmorphismCard>
              </motion.div>

              {/* Visualize Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="pt-4"
              >
                <Button
                  onClick={() => router.push(`/visual?topic=${encodeURIComponent(topic)}`)}
                  className="w-full"
                  size="lg"
                >
                  Visualize Topic
                </Button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
