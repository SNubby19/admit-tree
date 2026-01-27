import { useMemo } from 'react';
import { format, parseISO, isToday, isPast, isFuture, differenceInDays } from 'date-fns';
import { ApplicationStep, UniversityProgram, BonusTask } from '@/types/application';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Calendar, Pin, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface TimelineTask {
  step: ApplicationStep;
  date: Date;
  isBonus: boolean;
}

interface TaskTimelineProps {
  program: UniversityProgram;
  onTaskClick?: (stepId: string, programId: string) => void;
  onUnpin: () => void;
}

export const TaskTimeline = ({ program, onTaskClick, onUnpin }: TaskTimelineProps) => {
  // Extract all tasks (steps + bonus tasks) in order, no filtering by date
  const timelineTasks = useMemo(() => {
    const tasks: TimelineTask[] = [];
    
    // Add regular steps in order
    program.steps.forEach(step => {
      tasks.push({
        step,
        date: step.dueDate ? parseISO(step.dueDate) : new Date(2099, 11, 31),
        isBonus: false,
      });
    });
    
    // Add bonus tasks in order
    program.bonusTasks?.forEach(bonusTask => {
      tasks.push({
        step: {
          id: bonusTask.id,
          title: bonusTask.title,
          description: bonusTask.description,
          //status: bonusTask.isComplete ? 'complete' : 'todo',
          status: bonusTask.status,
          priority: 'low',
          dueDate: undefined,
        },
        date: new Date(2099, 11, 31), // Far future date for sorting
        isBonus: true,
      });
    });
    
    // Don't sort - keep original order
    return tasks;
  }, [program]);

  const getStatusStyles = (status: string, date: Date, isBonus: boolean) => {
    if (status === 'complete') {
      return 'bg-[hsl(var(--status-complete))] border-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))]';
    }

    if (isPast(date) && status !== 'complete') {
      return 'bg-destructive border-destructive text-destructive-foreground';
    }
    if (status === 'todo') {
      return 'bg-gray-500/10 border-gray-500/10 text-foreground';
    }
    if (status === 'in-progress') {
      return 'bg-[hsl(var(--status-in-progress))] border-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))]';
    }
    return 'bg-card border-border text-foreground';
  };

  const getDaysLabel = (date: Date) => {
    const days = differenceInDays(date, new Date());
    if (isToday(date)) return 'Today';
    if (days === 1) return 'Tomorrow';
    if (days === -1) return 'Yesterday';
    if (days < 0) return `${Math.abs(days)}d overdue`;
    return `${days}d left`;
  };

  if (timelineTasks.length === 0) {
    return null;
  }

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4 text-muted-foreground" />
          <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">
            {program.universityName} - {program.programName}
          </h3>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onUnpin}
          className="gap-2"
        >
          <Pin className="h-4 w-4 fill-current" />
          Unpin
        </Button>
      </div>
      
      <div className="bg-card border-2 border-border p-4">
        <ScrollArea className="w-full">
          <div className="flex gap-4 pb-3 min-w-max">
            {timelineTasks.map((task, index) => {
              const isOverdue = isPast(task.date) && task.step.status !== 'complete';
              const isComplete = task.step.status === 'complete';
              
              return (
                <div
                  key={`${task.step.id}-${index}`}
                  className={cn(
                    "relative flex-shrink-0 w-48 p-3 border-2 transition-all cursor-pointer hover:translate-y-[-2px] hover:shadow-md",
                    getStatusStyles(task.step.status, task.date, task.isBonus)
                  )}
                  onClick={() => {
                    if (onTaskClick) {
                      onTaskClick(task.step.id, program.id);
                    }
                  }}
                >
                  {/* Date Header */}
                  <div className="flex items-center justify-between mb-2">
                    {task.step.dueDate ? (
                      <>
                        <span className="text-xs font-mono font-bold">
                          {format(task.date, 'MMM d')}
                        </span>
                        <span className={cn(
                          "text-xs font-mono",
                          isOverdue && "text-destructive-foreground font-bold",
                          isComplete && "text-[hsl(var(--status-complete-foreground))]"
                        )}>
                          {getDaysLabel(task.date)}
                        </span>
                      </>
                    ) : (
                      <span className="text-xs font-mono text-muted-foreground">
                        No deadline
                      </span>
                    )}
                  </div>
                  
                  {/* Task Title */}
                  <p className="text-sm font-semibold line-clamp-2 mb-1">
                    {task.step.title}
                  </p>
                  
                  {/* Bonus indicator */}
                  {task.isBonus && (
                    <p className="text-xs opacity-80">
                      ⭐ Bonus Task
                    </p>
                  )}
                  
                  {/* Status Icon */}
                  <div className="absolute top-2 right-2">
                    {isComplete ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : isOverdue ? (
                      <AlertCircle className="h-4 w-4" />
                    ) : (
                      <Clock className="h-4 w-4 opacity-60" />
                    )}
                  </div>
                  
                  {/* Timeline connector */}
                  {index < timelineTasks.length - 1 && (
                    <div className="absolute right-[-1rem] top-1/2 w-4 h-0.5 bg-border" />
                  )}
                </div>
              );
            })}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </div>
    </div>
  );
};
