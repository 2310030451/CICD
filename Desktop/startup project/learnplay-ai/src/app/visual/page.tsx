'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { ArrowLeft, Play, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Visual() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [topic, setTopic] = useState(searchParams.get('topic') || '');
  const [scale, setScale] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [visualContent, setVisualContent] = useState<any>(null);

  useEffect(() => {
    if (topic) {
      generateVisualContent();
    }
  }, [topic]);

  const generateVisualContent = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setVisualContent({
        mindMap: {
          center: topic,
          branches: [
            { label: 'Concept 1', subPoints: ['Detail A', 'Detail B'] },
            { label: 'Concept 2', subPoints: ['Detail C', 'Detail D'] },
            { label: 'Concept 3', subPoints: ['Detail E', 'Detail F'] },
            { label: 'Concept 4', subPoints: ['Detail G', 'Detail H'] },
          ]
        },
        diagram: 'Interactive diagram showing the relationship between key concepts'
      });
      setIsGenerating(false);
    }, 2000);
  };

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.2, 2));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.2, 0.5));

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
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.back()}
              className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <h1 className="text-xl font-bold gradient-text">Visual Learning</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleZoomOut}
              className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <ZoomOut className="w-5 h-5" />
            </button>
            <button
              onClick={handleZoomIn}
              className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <ZoomIn className="w-5 h-5" />
            </button>
          </div>
        </motion.div>

        {/* Loading State */}
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center justify-center py-12"
          >
            <Mascot size={80} className="animate-float mb-4" />
            <p className="text-gray-400">Generating visual content...</p>
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mt-4" />
          </motion.div>
        )}

        {/* Visual Content */}
        {visualContent && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            {/* Mind Map */}
            <GlassmorphismCard className="p-6">
              <h3 className="font-semibold gradient-text mb-4 flex items-center gap-2">
                <Maximize2 className="w-5 h-5" />
                Mind Map
              </h3>
              <div 
                className="relative min-h-[400px] bg-white/5 rounded-xl p-4 overflow-hidden"
                style={{ transform: `scale(${scale})`, transformOrigin: 'center' }}
              >
                {/* Center Node */}
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 gradient-bg text-white px-6 py-3 rounded-full font-bold shadow-lg"
                >
                  {visualContent.mindMap.center}
                </motion.div>

                {/* Branches */}
                {visualContent.mindMap.branches.map((branch: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="absolute"
                    style={{
                      top: `${25 + (index % 2) * 50}%`,
                      left: index < 2 ? '10%' : '75%',
                      transform: 'translate(-50%, -50%)'
                    }}
                  >
                    <div className="glassmorphism px-4 py-2 rounded-lg">
                      <p className="font-medium text-sm mb-2">{branch.label}</p>
                      {branch.subPoints.map((point: string, pIndex: number) => (
                        <div key={pIndex} className="text-xs text-gray-400 flex items-center gap-1">
                          <span className="w-1 h-1 bg-primary rounded-full" />
                          {point}
                        </div>
                      ))}
                    </div>
                  </motion.div>
                ))}

                {/* Connection Lines */}
                <svg className="absolute inset-0 w-full h-full pointer-events-none">
                  {visualContent.mindMap.branches.map((branch: any, index: number) => (
                    <motion.line
                      key={index}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 0.3 }}
                      transition={{ delay: 0.4 + index * 0.1 }}
                      x1="50%"
                      y1="50%"
                      x2={index < 2 ? "15%" : "85%"}
                      y2={`${25 + (index % 2) * 50}%`}
                      stroke="#6C63FF"
                      strokeWidth="2"
                      strokeDasharray="5,5"
                    />
                  ))}
                </svg>
              </div>
            </GlassmorphismCard>

            {/* Animated Diagram */}
            <GlassmorphismCard className="p-6">
              <h3 className="font-semibold gradient-text mb-4">Interactive Diagram</h3>
              <div className="bg-white/5 rounded-xl p-6 min-h-[200px] flex items-center justify-center">
                <motion.div
                  animate={{
                    rotate: [0, 360],
                  }}
                  transition={{
                    duration: 20,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                  className="relative w-32 h-32"
                >
                  <div className="absolute inset-0 border-4 border-primary rounded-full" />
                  <div className="absolute inset-4 border-4 border-secondary rounded-full" />
                  <div className="absolute inset-8 border-4 border-accent rounded-full" />
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 gradient-bg rounded-full" />
                </motion.div>
              </div>
              <p className="text-gray-400 text-sm text-center mt-4">{visualContent.diagram}</p>
            </GlassmorphismCard>

            {/* Flowchart */}
            <GlassmorphismCard className="p-6">
              <h3 className="font-semibold gradient-text mb-4">Flowchart</h3>
              <div className="space-y-3">
                {['Start', 'Process Step 1', 'Decision Point', 'Process Step 2', 'End'].map((step, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="flex items-center gap-3"
                  >
                    <div className={`w-3 h-3 rounded-full ${
                      index === 0 ? 'bg-green-500' : index === 4 ? 'bg-red-500' : 'bg-primary'
                    }`} />
                    <div className="glassmorphism px-4 py-2 rounded-lg flex-1">
                      <span className="text-sm">{step}</span>
                    </div>
                    {index < 4 && (
                      <div className="w-8 h-0.5 bg-primary/30" />
                    )}
                  </motion.div>
                ))}
              </div>
            </GlassmorphismCard>

            {/* Watch Animation Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="pt-4"
            >
              <Button
                onClick={() => router.push(`/animation?topic=${encodeURIComponent(topic)}`)}
                className="w-full"
                size="lg"
              >
                <Play className="w-5 h-5 mr-2" />
                Watch Animation
              </Button>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
