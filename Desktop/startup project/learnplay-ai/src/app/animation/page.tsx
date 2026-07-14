'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { ArrowLeft, Play, Pause, Volume2, Settings, Clock } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Animation() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [topic, setTopic] = useState(searchParams.get('topic') || '');
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [speed, setSpeed] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [videoContent, setVideoContent] = useState<any>(null);

  useEffect(() => {
    if (topic) {
      generateVideoContent();
    }
  }, [topic]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying && progress < 100) {
      interval = setInterval(() => {
        setProgress(prev => Math.min(prev + (0.5 * speed), 100));
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlaying, progress, speed]);

  const generateVideoContent = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setVideoContent({
        title: `${topic} - Animated Explanation`,
        duration: '3:45',
        narration: `Welcome to this animated explanation of ${topic}. Let's explore this fascinating concept together through visual storytelling.`,
        subtitles: [
          { time: '0:00', text: 'Introduction to the topic' },
          { time: '0:30', text: 'Key concept breakdown' },
          { time: '1:15', text: 'Real-world applications' },
          { time: '2:00', text: 'Interactive examples' },
          { time: '2:45', text: 'Summary and key takeaways' },
        ]
      });
      setIsGenerating(false);
    }, 2000);
  };

  const handlePlayPause = () => setIsPlaying(!isPlaying);
  const handleSpeedChange = () => {
    const speeds = [0.5, 1, 1.5, 2];
    const currentIndex = speeds.indexOf(speed);
    setSpeed(speeds[(currentIndex + 1) % speeds.length]);
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
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.back()}
              className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <h1 className="text-xl font-bold gradient-text">Animated Video</h1>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Clock className="w-4 h-4" />
            {videoContent?.duration || '0:00'}
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
            <p className="text-gray-400">Generating animated video...</p>
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mt-4" />
          </motion.div>
        )}

        {/* Video Content */}
        {videoContent && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            {/* Video Player */}
            <GlassmorphismCard className="p-4">
              <div className="relative aspect-video bg-gradient-to-br from-primary/20 to-accent/20 rounded-xl overflow-hidden mb-4">
                {/* Animated Background */}
                <motion.div
                  animate={{
                    backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'],
                  }}
                  transition={{
                    duration: 10,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                  className="absolute inset-0 bg-[length:200%_200%]"
                  style={{
                    backgroundImage: 'radial-gradient(circle at 20% 50%, rgba(108, 99, 255, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 50%, rgba(0, 217, 255, 0.3) 0%, transparent 50%)'
                  }}
                />
                
                {/* Play Button Overlay */}
                {!isPlaying && (
                  <motion.button
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={handlePlayPause}
                    className="absolute inset-0 flex items-center justify-center"
                  >
                    <div className="w-20 h-20 gradient-bg rounded-full flex items-center justify-center shadow-lg animate-glow">
                      <Play className="w-10 h-10 text-white ml-1" />
                    </div>
                  </motion.button>
                )}

                {/* Playing Animation */}
                {isPlaying && (
                  <motion.div
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.5, 1, 0.5],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                    }}
                    className="absolute inset-0 flex items-center justify-center"
                  >
                    <Mascot size={60} />
                  </motion.div>
                )}

                {/* Subtitle Overlay */}
                {isPlaying && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="absolute bottom-4 left-4 right-4 glassmorphism-dark p-3 rounded-lg"
                  >
                    <p className="text-sm text-white text-center">
                      {videoContent.subtitles[Math.floor(progress / 20)]?.text || 'Playing...'}
                    </p>
                  </motion.div>
                )}
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="w-full bg-white/10 rounded-full h-2 mb-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    className="gradient-bg h-2 rounded-full"
                  />
                </div>
                <div className="flex justify-between text-xs text-gray-400">
                  <span>{Math.floor(progress * 0.0225)}:00</span>
                  <span>{videoContent.duration}</span>
                </div>
              </div>

              {/* Controls */}
              <div className="flex items-center justify-between">
                <button
                  onClick={handlePlayPause}
                  className="glassmorphism p-3 rounded-full hover:bg-white/10 transition-colors"
                >
                  {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-1" />}
                </button>

                <div className="flex items-center gap-2">
                  <Volume2 className="w-5 h-5 text-gray-400" />
                  <div className="w-24 bg-white/10 rounded-full h-1">
                    <div className="w-3/4 gradient-bg h-1 rounded-full" />
                  </div>
                </div>

                <button
                  onClick={handleSpeedChange}
                  className="glassmorphism px-4 py-2 rounded-full hover:bg-white/10 transition-colors text-sm font-medium"
                >
                  {speed}x
                </button>

                <button className="glassmorphism p-3 rounded-full hover:bg-white/10 transition-colors">
                  <Settings className="w-5 h-5" />
                </button>
              </div>
            </GlassmorphismCard>

            {/* Video Info */}
            <GlassmorphismCard className="p-5">
              <h3 className="font-semibold gradient-text mb-2">{videoContent.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{videoContent.narration}</p>
            </GlassmorphismCard>

            {/* Subtitle Timeline */}
            <GlassmorphismCard className="p-5">
              <h3 className="font-semibold gradient-text mb-4">Subtitles</h3>
              <div className="space-y-2">
                {videoContent.subtitles.map((subtitle: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 * index }}
                    className={`flex items-center gap-3 p-3 rounded-lg ${
                      progress >= index * 20 && progress < (index + 1) * 20 ? 'bg-primary/20' : 'bg-white/5'
                    }`}
                  >
                    <span className="text-xs text-gray-400 w-12">{subtitle.time}</span>
                    <span className="text-sm flex-1">{subtitle.text}</span>
                  </motion.div>
                ))}
              </div>
            </GlassmorphismCard>

            {/* Generate Memory Tricks Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="pt-4"
            >
              <Button
                onClick={() => router.push(`/memory?topic=${encodeURIComponent(topic)}`)}
                className="w-full"
                size="lg"
              >
                Generate Memory Tricks
              </Button>
            </motion.div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
