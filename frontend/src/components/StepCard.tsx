import { ApplicationStep, TaskStatus } from '@/types/application';
import { Calendar, AlertCircle, Star, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { isPast, parseISO } from 'date-fns';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface StepCardProps {
  step: ApplicationStep;
  index: number;
  isBonus?: boolean;
  onStatusChange?: (newStatus: TaskStatus) => void;
}

const statusConfig: Record<TaskStatus, { label: string; cardClass: string }> = {
  'todo': {
    label: 'To Do',
    cardClass: 'bg-card',
  },
  'in-progress': {
    label: 'In Progress',
    cardClass: 'bg-[hsl(var(--status-in-progress))]',
  },
  'complete': {
    label: 'Done',
    cardClass: 'bg-[hsl(var(--status-complete))]',
  },
};

export function StepCard({ step, index, isBonus = false, onStatusChange }: StepCardProps) {
  const handleStatusChange = (newStatus: TaskStatus) => {
    if (onStatusChange) {
      onStatusChange(newStatus);
    }
  };

  // Ensure status is valid, default to 'todo' if undefined
  const currentStatus: TaskStatus = step.status || 'todo';

  // Check if deadline is past
  const isOverdue = step.dueDate && isPast(parseISO(step.dueDate)) && currentStatus !== 'complete';

  return (
    <div
      className={cn(
        'border-2 border-border p-4 shadow-xs hover:shadow-sm transition-shadow',
        isBonus && 'bg-yellow-50/5',
        isOverdue ? 'bg-destructive text-destructive-foreground' : statusConfig[currentStatus].cardClass
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className={cn(
            "flex items-center justify-center w-8 h-8 font-mono font-bold text-sm border-2 border-border flex-shrink-0",
            isBonus ? "bg-yellow-500 text-black" : "bg-primary text-primary-foreground"
          )}>
            {isBonus ? <Star className="h-4 w-4" /> : index + 1}
          </div>
          <div className="flex-1 min-w-0">
            <h4 className={cn("font-bold text-sm", (isOverdue || currentStatus === 'complete') && "text-white")}>{step.title}</h4>
            <p className={cn("text-xs mb-2", isOverdue ? "text-white/90" : "text-muted-foreground")}>{step.description}</p>
            {step.dueDate && (
              <div className={cn("flex items-center gap-1 text-xs", isOverdue ? "text-white/90" : "text-muted-foreground")}>
                <Calendar className="h-3 w-3" />
                <span className="font-mono">{step.dueDate}</span>
              </div>
            )}
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild disabled={isOverdue}>
              <button 
                className={cn(
                  "inline-flex items-center gap-1 px-2 py-0.5 text-xs font-mono font-bold uppercase tracking-wider border-2 border-border transition-colors",
                  isOverdue 
                    ? "bg-destructive/50 text-destructive-foreground cursor-not-allowed opacity-50" 
                    : "bg-muted text-muted-foreground hover:bg-accent"
                )}
                disabled={isOverdue}
              >
                {statusConfig[currentStatus].label}
                <ChevronDown className="h-3 w-3" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => handleStatusChange('todo')}>
                To Do
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleStatusChange('in-progress')}>
                In Progress
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleStatusChange('complete')}>
                Done
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          {(step.priority === 'high' || isOverdue) && currentStatus !== 'complete' && !isBonus && (
            <AlertCircle className={cn("h-4 w-4", isOverdue ? "text-white" : "text-destructive")} />
          )}
        </div>
      </div>
    </div>
  );
}
