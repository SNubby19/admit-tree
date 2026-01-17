import { useState } from 'react';
import { mockPrograms, globalBonusTasks, applicationRoadmaps } from '@/data/mockData';
import { DashboardHeader } from '@/components/DashboardHeader';
import { ProgramCard } from '@/components/ProgramCard';
import { BonusTaskCard } from '@/components/BonusTaskCard';
import { RoadmapSidebar } from '@/components/RoadmapSidebar';
import { ChatbotButton } from '@/components/ChatbotButton';
import { FocusedProgramView } from '@/components/FocusedProgramView';
import { TaskTimeline } from '@/components/TaskTimeline';
import { Star } from 'lucide-react';

const Index = () => {
  const [focusedProgramId, setFocusedProgramId] = useState<string | null>(null);
  const [activeRoadmapId, setActiveRoadmapId] = useState<string | null>(null);

  // Calculate stats
  const totalPrograms = mockPrograms.length;
  const allSteps = mockPrograms.flatMap(p => p.steps);
  const completedSteps = allSteps.filter(s => s.status === 'complete').length;
  const totalSteps = allSteps.length;
  const overallProgress = Math.round((completedSteps / totalSteps) * 100);

  const completedBonusTasks = globalBonusTasks.filter(t => t.isComplete).length;

  // Get focused program
  const focusedProgram = focusedProgramId 
    ? mockPrograms.find(p => p.id === focusedProgramId) 
    : null;

  // Filter programs by active roadmap
  const activeRoadmap = activeRoadmapId 
    ? applicationRoadmaps.find(r => r.id === activeRoadmapId)
    : null;
  
  const displayedPrograms = activeRoadmap
    ? mockPrograms.filter(p => activeRoadmap.programIds.includes(p.id))
    : mockPrograms;

  const handleSelectRoadmap = (id: string) => {
    setActiveRoadmapId(id === activeRoadmapId ? null : id);
    setFocusedProgramId(null);
  };

  const handleCreateRoadmap = () => {
    // TODO: Implement roadmap creation modal
    console.log('Create new roadmap');
  };

  const handleProgramClick = (programId: string) => {
    setFocusedProgramId(programId);
  };

  const handleTimelineTaskClick = (stepId: string, programId: string) => {
    setFocusedProgramId(programId);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container max-w-6xl py-8 px-4">
        <div className="flex items-center gap-4 mb-6">
          <RoadmapSidebar
            roadmaps={applicationRoadmaps}
            activeRoadmapId={activeRoadmapId}
            onSelectRoadmap={handleSelectRoadmap}
            onCreateRoadmap={handleCreateRoadmap}
          />
          {activeRoadmap && (
            <span className="text-sm text-muted-foreground font-mono">
              Viewing: {activeRoadmap.name}
            </span>
          )}
        </div>

        {/* Timeline at the top */}
        {!focusedProgram && (
          <TaskTimeline 
            programs={displayedPrograms} 
            onTaskClick={handleTimelineTaskClick}
          />
        )}

        {focusedProgram ? (
          <FocusedProgramView
            program={focusedProgram}
            onBack={() => setFocusedProgramId(null)}
          />
        ) : (
          <>
            <DashboardHeader
              totalPrograms={displayedPrograms.length}
              overallProgress={overallProgress}
              completedTasks={completedSteps}
              totalTasks={totalSteps}
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Main Content - Program Cards */}
              <div className="lg:col-span-2 space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold uppercase tracking-wider">
                    {activeRoadmap ? activeRoadmap.name : 'My Programs'}
                  </h2>
                  <span className="text-sm text-muted-foreground font-mono">
                    {displayedPrograms.length} active
                  </span>
                </div>
                {displayedPrograms.length > 0 ? (
                  displayedPrograms.map(program => (
                    <div 
                      key={program.id} 
                      onClick={() => handleProgramClick(program.id)}
                      className="cursor-pointer"
                    >
                      <ProgramCard program={program} />
                    </div>
                  ))
                ) : (
                  <div className="bg-card border-2 border-border p-8 text-center">
                    <p className="text-muted-foreground">No programs in this roadmap yet.</p>
                  </div>
                )}
              </div>

              {/* Sidebar - Bonus Tasks */}
              <div className="lg:col-span-1">
                <div className="sticky top-8">
                  <div className="bg-card border-2 border-border shadow-sm">
                    <div className="p-4 border-b-2 border-border bg-[hsl(var(--status-bonus))]">
                      <div className="flex items-center gap-2 text-[hsl(var(--status-bonus-foreground))]">
                        <Star className="h-5 w-5" />
                        <h2 className="font-bold uppercase tracking-wider">Bonus Tasks</h2>
                      </div>
                      <p className="text-[hsl(var(--status-bonus-foreground))] text-xs mt-1 opacity-90">
                        Strengthen your application profile
                      </p>
                    </div>
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-sm text-muted-foreground">Completed</span>
                        <span className="font-mono font-bold">{completedBonusTasks}/{globalBonusTasks.length}</span>
                      </div>
                      <div className="space-y-3">
                        {globalBonusTasks.map(task => (
                          <BonusTaskCard key={task.id} task={task} />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Chatbot Button */}
      <ChatbotButton />
    </div>
  );
};

export default Index;
