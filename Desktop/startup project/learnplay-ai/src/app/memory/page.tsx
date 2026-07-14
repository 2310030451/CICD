'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { ArrowLeft, Brain, Lightbulb, Music, BookMarked } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Memory() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [topic, setTopic] = useState(searchParams.get('topic') || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [memoryContent, setMemoryContent] = useState<any>(null);
  const [flippedCards, setFlippedCards] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (topic) {
      generateMemoryContent();
    }
  }, [topic]);

  const generateMemoryContent = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setMemoryContent({
        mnemonics: [
          { acronym: 'SMART', meaning: 'Specific, Measurable, Achievable, Relevant, Time-bound' },
          { acronym: 'ROYGBIV', meaning: 'Red, Orange, Yellow, Green, Blue, Indigo, Violet (Colors)' },
        ],
        funnyStory: `Imagine ${topic} as a character in a story. This character goes on an adventure where they meet different concepts along the way. Each encounter teaches them something new about ${topic}, making it easier to remember!`,
        rhymes: [
          `${topic} is the key, to understanding what we see`,
          `Learn it well, and you'll excel, in ${topic} stories we tell`
        ],
        memoryCards: [
          { front: 'Key Concept 1', back: 'Detailed explanation of the first important concept' },
          { front: 'Key Concept 2', back: 'Detailed explanation of the second important concept' },
          { front: 'Key Concept 3', back: 'Detailed explanation of the third important concept' },
          { front: 'Key Concept 4', back: 'Detailed explanation of the fourth important concept' },
        ]
      });
      setIsGenerating(false);
    }, 2000);
  };

  const handleCardFlip = (index: number) => {
    setFlippedCards(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
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
          <h1 className="text-xl font-bold gradient-text">Memory Tricks</h1>
        </motion.div>

        {/* Loading State */}
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center justify-center py-12"
          >
            <Mascot size={80} className="animate-float mb-4" />
            <p className="text-gray-400">Creating memory tricks...</p>
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mt-4" />
          </motion.div>
        )}

        {/* Memory Content */}
        {memoryContent && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            {/* Mnemonics */}
            <GlassmorphismCard className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <Brain className="w-5 h-5 text-primary" />
                <h3 className="font-semibold gradient-text">Mnemonics</h3>
              </div>
              <div className="space-y-3">
                {memoryContent.mnemonics.map((mnemonic: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 * index }}
                    className="glassmorphism p-4 rounded-lg"
                  >
                    <div className="text-2xl font-bold gradient-text mb-2">{mnemonic.acronym}</div>
                    <p className="text-sm text-gray-300">{mnemonic.meaning}</p>
                  </motion.div>
                ))}
              </div>
            </GlassmorphismCard>

            {/* Funny Story */}
            <GlassmorphismCard className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="w-5 h-5 text-accent" />
                <h3 className="font-semibold gradient-text">Funny Story</h3>
              </div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glassmorphism p-4 rounded-lg"
              >
                <p className="text-gray-300 leading-relaxed">{memoryContent.funnyStory}</p>
              </motion.div>
            </GlassmorphismCard>

            {/* Rhymes */}
            <GlassmorphismCard className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <Music className="w-5 h-5 text-secondary" />
                <h3 className="font-semibold gradient-text">Rhymes</h3>
              </div>
              <div className="space-y-3">
                {memoryContent.rhymes.map((rhyme: string, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + index * 0.1 }}
                    className="glassmorphism p-4 rounded-lg"
                  >
                    <p className="text-gray-300 italic">"{rhyme}"</p>
                  </motion.div>
                ))}
              </div>
            </GlassmorphismCard>

            {/* Memory Cards */}
            <GlassmorphismCard className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <BookMarked className="w-5 h-5 text-primary" />
                <h3 className="font-semibold gradient-text">Memory Cards</h3>
                <span className="text-xs text-gray-400 ml-auto">Tap to flip</span>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {memoryContent.memoryCards.map((card: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="perspective-1000"
                  >
                    <motion.div
                      className="relative w-full h-32 cursor-pointer"
                      onClick={() => handleCardFlip(index)}
                      animate={{ rotateY: flippedCards.has(index) ? 180 : 0 }}
                      transition={{ duration: 0.6 }}
                      style={{ transformStyle: 'preserve-3d' }}
                    >
                      <div
                        className={`absolute inset-0 glassmorphism p-4 rounded-lg flex items-center justify-center text-center backface-hidden ${
                          flippedCards.has(index) ? 'rotate-y-180' : ''
                        }`}
                        style={{ backfaceVisibility: 'hidden' }}
                      >
                        <span className="font-medium text-sm">{card.front}</span>
                      </div>
                      <div
                        className="absolute inset-0 glassmorphism-dark p-4 rounded-lg flex items-center justify-center text-center backface-hidden rotate-y-180"
                        style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
                      >
                        <span className="text-sm text-gray-300">{card.back}</span>
                      </div>
                    </motion.div>
                  </motion.div>
                ))}
              </div>
            </GlassmorphismCard>

            {/* Take Quiz Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
              className="pt-4"
            >
              <Button
                onClick={() => router.push(`/quiz?topic=${encodeURIComponent(topic)}`)}
                className="w-full"
                size="lg"
              >
                Take Quiz
              </Button>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
