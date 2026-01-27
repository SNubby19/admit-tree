import { useState } from 'react';
import { UniversityProgram } from '@/types/application';
import { ProgressBar } from './ProgressBar';
import { StepCard } from './StepCard';
import { Pin, Calendar, GraduationCap } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ProgramCardProps {
  program: UniversityProgram;
  isPinned: boolean;
  onTogglePin: () => void;
  onClick: () => void;
}

export function ProgramCard({ program, isPinned, onTogglePin, onClick }: ProgramCardProps) {
  const completedSteps = program.steps.filter(s => s.status === 'complete').length;
  const inProgressSteps = program.steps.filter(s => s.status === 'in-progress').length;
  const todoSteps = program.steps.filter(s => s.status === 'todo').length;

  return (
    <div className="bg-card border-2 border-border shadow-sm hover:shadow-md transition-shadow">
      {/* Card Header - Always Visible */}
      <div
        onClick={onClick}
        className="w-full p-5 text-left hover:bg-accent/50 transition-colors cursor-pointer"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <GraduationCap className="h-5 w-5 flex-shrink-0" />
              <h3 className="font-bold text-lg truncate">{program.universityName}</h3>
            </div>
            <p className="text-muted-foreground font-medium mb-3">{program.programName}</p>
            
            <div className="flex items-center gap-4 text-sm mb-4">
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <Calendar className="h-4 w-4" />
                <span className="font-mono">{program.deadline}</span>
              </div>
            </div>

            <ProgressBar value={program.overallProgress} />
          </div>
          
          <div className="flex flex-col items-end gap-2">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onTogglePin();
              }}
              className="p-1 hover:opacity-70 transition-opacity"
              title={isPinned ? "Unpin from timeline" : "Pin to timeline"}
            >
              <Pin className={cn("h-5 w-5", isPinned ? "fill-black text-black" : "text-muted-foreground")} />
            </button>
          </div>
        </div>

        {/* Status Summary Pills */}
        <div className="flex flex-wrap gap-2 mt-4">
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] text-xs font-mono font-bold border-2 border-border">
            {completedSteps} Done
          </span>
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] text-xs font-mono font-bold border-2 border-border">
            {inProgressSteps} In Progress
          </span>
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-muted text-muted-foreground text-xs font-mono font-bold border-2 border-border">
            {todoSteps} To Do
          </span>
        </div>
      </div>
    </div>
  );
}
