'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, CheckCircle, XCircle, Trophy, Zap, Coins } from 'lucide-react';
import Mascot from '@/components/Mascot';
import Particles from '@/components/Particles';
import Button from '@/components/Button';
import GlassmorphismCard from '@/components/GlassmorphismCard';

export default function Quiz() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [topic, setTopic] = useState(searchParams.get('topic') || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [quizData, setQuizData] = useState<any>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [xpEarned, setXpEarned] = useState(0);
  const [coinsEarned, setCoinsEarned] = useState(0);
  const [accuracy, setAccuracy] = useState(0);

  useEffect(() => {
    generateQuizData();
  }, [topic]);

  const generateQuizData = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setQuizData({
        questions: [
          {
            type: 'mcq',
            question: `What is the primary purpose of ${topic}?`,
            options: [
              'To understand complex concepts',
              'To memorize information',
              'To solve problems efficiently',
              'All of the above'
            ],
            correctAnswer: 3
          },
          {
            type: 'trueFalse',
            question: `${topic} is essential for modern learning.`,
            options: ['True', 'False'],
            correctAnswer: 0
          },
          {
            type: 'fillBlank',
            question: `${topic} helps us understand ______ better.`,
            options: ['the world', 'nothing', 'only math', 'only science'],
            correctAnswer: 0
          },
          {
            type: 'mcq',
            question: `Which of these is NOT related to ${topic}?`,
            options: [
              'Critical thinking',
              'Problem solving',
              'Random guessing',
              'Logical reasoning'
            ],
            correctAnswer: 2
          },
          {
            type: 'trueFalse',
            question: `${topic} can be learned through visual aids.`,
            options: ['True', 'False'],
            correctAnswer: 0
          }
        ]
      });
      setIsGenerating(false);
    }, 2000);
  };

  const handleAnswerSelect = (answerIndex: number) => {
    if (showResult) return;
    setSelectedAnswer(answerIndex);
    setShowResult(true);

    const isCorrect = answerIndex === quizData.questions[currentQuestion].correctAnswer;
    if (isCorrect) {
      setScore(prev => prev + 1);
      setXpEarned(prev => prev + 50);
      setCoinsEarned(prev => prev + 10);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestion < quizData.questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      // Calculate final accuracy
      const finalAccuracy = Math.round((score / quizData.questions.length) * 100);
      setAccuracy(finalAccuracy);
      router.push(`/rewards?xp=${xpEarned}&coins=${coinsEarned}&accuracy=${finalAccuracy}&score=${score}`);
    }
  };

  const getCurrentQuestionType = () => {
    if (!quizData) return '';
    const type = quizData.questions[currentQuestion].type;
    switch (type) {
      case 'mcq': return 'Multiple Choice';
      case 'trueFalse': return 'True / False';
      case 'fillBlank': return 'Fill in the Blank';
      default: return 'Question';
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
          className="flex items-center justify-between mb-6"
        >
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.back()}
              className="glassmorphism p-2 rounded-full hover:bg-white/10 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <h1 className="text-xl font-bold gradient-text">Quiz</h1>
          </div>
          <div className="flex gap-2">
            <div className="glassmorphism px-3 py-2 flex items-center gap-1">
              <Zap className="w-4 h-4 text-accent" />
              <span className="text-sm font-semibold">{xpEarned}</span>
            </div>
            <div className="glassmorphism px-3 py-2 flex items-center gap-1">
              <Coins className="w-4 h-4 text-yellow-500" />
              <span className="text-sm font-semibold">{coinsEarned}</span>
            </div>
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
            <p className="text-gray-400">Generating quiz questions...</p>
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mt-4" />
          </motion.div>
        )}

        {/* Quiz Content */}
        {quizData && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            {/* Progress */}
            <GlassmorphismCard className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-400">
                  Question {currentQuestion + 1} of {quizData.questions.length}
                </span>
                <span className="text-sm font-medium gradient-text">{getCurrentQuestionType()}</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${((currentQuestion + 1) / quizData.questions.length) * 100}%` }}
                  className="gradient-bg h-2 rounded-full"
                />
              </div>
            </GlassmorphismCard>

            {/* Question */}
            <GlassmorphismCard className="p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={currentQuestion}
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -50 }}
                  transition={{ duration: 0.3 }}
                >
                  <h3 className="text-lg font-semibold mb-6">{quizData.questions[currentQuestion].question}</h3>
                  
                  <div className="space-y-3">
                    {quizData.questions[currentQuestion].options.map((option: string, index: number) => {
                      let borderColor = 'border-white/10';
                      let bgColor = 'bg-white/5';
                      
                      if (showResult) {
                        if (index === quizData.questions[currentQuestion].correctAnswer) {
                          borderColor = 'border-green-500';
                          bgColor = 'bg-green-500/20';
                        } else if (index === selectedAnswer && index !== quizData.questions[currentQuestion].correctAnswer) {
                          borderColor = 'border-red-500';
                          bgColor = 'bg-red-500/20';
                        }
                      } else if (selectedAnswer === index) {
                        borderColor = 'border-primary';
                        bgColor = 'bg-primary/20';
                      }

                      return (
                        <motion.button
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          onClick={() => handleAnswerSelect(index)}
                          disabled={showResult}
                          className={`w-full p-4 rounded-xl border-2 ${borderColor} ${bgColor} text-left transition-all hover:scale-[1.02] disabled:hover:scale-100`}
                        >
                          <div className="flex items-center gap-3">
                            <span className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm font-medium">
                              {String.fromCharCode(65 + index)}
                            </span>
                            <span className="flex-1">{option}</span>
                            {showResult && index === quizData.questions[currentQuestion].correctAnswer && (
                              <CheckCircle className="w-5 h-5 text-green-500" />
                            )}
                            {showResult && selectedAnswer === index && index !== quizData.questions[currentQuestion].correctAnswer && (
                              <XCircle className="w-5 h-5 text-red-500" />
                            )}
                          </div>
                        </motion.button>
                      );
                    })}
                  </div>
                </motion.div>
              </AnimatePresence>
            </GlassmorphismCard>

            {/* Next Button */}
            {showResult && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="pt-4"
              >
                <Button
                  onClick={handleNextQuestion}
                  className="w-full"
                  size="lg"
                >
                  {currentQuestion < quizData.questions.length - 1 ? 'Next Question' : 'View Rewards'}
                </Button>
              </motion.div>
            )}

            {/* Score Display */}
            <GlassmorphismCard className="p-4">
              <div className="flex items-center justify-around">
                <div className="text-center">
                  <Trophy className="w-6 h-6 text-yellow-500 mx-auto mb-1" />
                  <p className="text-2xl font-bold gradient-text">{score}</p>
                  <p className="text-xs text-gray-400">Score</p>
                </div>
                <div className="text-center">
                  <Zap className="w-6 h-6 text-accent mx-auto mb-1" />
                  <p className="text-2xl font-bold gradient-text">{xpEarned}</p>
                  <p className="text-xs text-gray-400">XP</p>
                </div>
                <div className="text-center">
                  <Coins className="w-6 h-6 text-yellow-500 mx-auto mb-1" />
                  <p className="text-2xl font-bold gradient-text">{coinsEarned}</p>
                  <p className="text-xs text-gray-400">Coins</p>
                </div>
              </div>
            </GlassmorphismCard>
          </motion.div>
        )}
      </div>
    </div>
  );
}
