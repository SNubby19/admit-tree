import { useState, useEffect } from 'react';
import { UniversityProgram, TaskStatus } from '@/types/application';
import { ProgressBar } from './ProgressBar';
import { StepCard } from './StepCard';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Calendar, GraduationCap, Clock } from 'lucide-react';

interface FocusedProgramViewProps {
  program: UniversityProgram;
  onBack: () => void;
  onProgramUpdate?: (updatedProgram: UniversityProgram) => void;
}

export function FocusedProgramView({ program, onBack, onProgramUpdate }: FocusedProgramViewProps) {
  const [localProgram, setLocalProgram] = useState(program);

  useEffect(() => {
    setLocalProgram(program);
  }, [program]);

  const completedSteps = localProgram.steps.filter(s => s.status === 'complete').length;
  const inProgressSteps = localProgram.steps.filter(s => s.status === 'in-progress').length;
  const todoSteps = localProgram.steps.filter(s => s.status === 'todo').length;
  const totalSteps = localProgram.steps.length;
  const overallProgress = totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;

  const handleStepStatusChange = (stepId: string, newStatus: TaskStatus) => {
    const updatedSteps = localProgram.steps.map(step =>
      step.id === stepId ? { ...step, status: newStatus } : step
    );

    const updatedProgram = {
      ...localProgram,
      steps: updatedSteps,
      overallProgress,
    };

    setLocalProgram(updatedProgram);
    
    if (onProgramUpdate) {
      onProgramUpdate(updatedProgram);
    }
  };

  const handleBonusTaskStatusChange = (taskId: string, newStatus: TaskStatus) => {
    const updatedBonusTasks = localProgram.bonusTasks?.map(task =>
      task.id === taskId ? { ...task, status: newStatus } : task
    );

    const updatedProgram = {
      ...localProgram,
      bonusTasks: updatedBonusTasks || [],
    };

    setLocalProgram(updatedProgram);
    
    if (onProgramUpdate) {
      onProgramUpdate(updatedProgram);
    }
  };

  // Calculate days until deadline
  const deadline = new Date(localProgram.deadline);
  const today = new Date();
  const daysUntilDeadline = Math.ceil((deadline.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Button
        variant="ghost"
        onClick={onBack}
        className="gap-2 font-bold uppercase tracking-wider text-sm hover:bg-transparent -ml-4"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to All Programs
      </Button>

      {/* Program Header */}
      <div className="bg-card border-2 border-border p-6 shadow-sm">
        <div className="flex items-start justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <GraduationCap className="h-8 w-8" />
              <div>
                <h1 className="text-2xl font-bold">{program.universityName}</h1>
                <p className="text-lg text-muted-foreground font-medium">{program.programName}</p>
              </div>
            </div>

            <div className="flex items-center gap-6 mt-6">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Calendar className="h-5 w-5" />
                <span className="font-mono font-bold">{program.deadline}</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                <span className={`font-mono font-bold ${daysUntilDeadline < 30 ? 'text-destructive' : 'text-muted-foreground'}`}>
                  {daysUntilDeadline > 0 ? `${daysUntilDeadline} days left` : 'Deadline passed'}
                </span>
              </div>
            </div>
          </div>

          <div className="text-right">
            <div className="text-4xl font-mono font-bold">{overallProgress}%</div>
            <p className="text-sm text-muted-foreground uppercase tracking-wider">Complete</p>
          </div>
        </div>

        <div className="mt-6">
          <ProgressBar value={overallProgress} />
        </div>

        {/* Status Summary */}
        <div className="flex flex-wrap gap-3 mt-6">
          <div className="flex items-center gap-2 px-4 py-2 bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] border-2 border-border">
            <span className="text-2xl font-mono font-bold">{completedSteps}</span>
            <span className="text-sm uppercase tracking-wider">Done</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] border-2 border-border">
            <span className="text-2xl font-mono font-bold">{inProgressSteps}</span>
            <span className="text-sm uppercase tracking-wider">In Progress</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-muted text-muted-foreground border-2 border-border">
            <span className="text-2xl font-mono font-bold">{todoSteps}</span>
            <span className="text-sm uppercase tracking-wider">To Do</span>
          </div>
        </div>
      </div>

      {/* Application Steps */}
      <div className="bg-card border-2 border-border shadow-sm">
        <div className="p-4 border-b-2 border-border bg-muted">
          <h2 className="font-bold uppercase tracking-wider">Application Steps</h2>
        </div>
        <div className="p-6 space-y-4">
          {localProgram.steps.map((step, index) => (
            <StepCard 
              key={step.id} 
              step={step} 
              index={index}
              onStatusChange={(newStatus) => handleStepStatusChange(step.id, newStatus)}
            />
          ))}
        </div>
      </div>

      {/* Bonus Tasks */}
      {program.bonusTasks && program.bonusTasks.length > 0 && (
        <div className="bg-card border-2 border-border shadow-sm">
          <div className="p-4 border-b-2 border-border bg-muted">
            <h2 className="font-bold uppercase tracking-wider">Bonus Tasks</h2>
          </div>
          <div className="p-6 space-y-4">
            {localProgram.bonusTasks.map((task, index) => (
              <StepCard 
                key={task.id} 
                step={{
                  id: task.id,
                  title: task.title,
                  description: task.description,
                  status: task.status,
                  priority: 'low',
                  dueDate: undefined
                }} 
                index={localProgram.steps.length + index}
                isBonus={true}
                onStatusChange={(newStatus) => handleBonusTaskStatusChange(task.id, newStatus)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
