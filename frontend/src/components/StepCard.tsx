import { ApplicationStep, TaskStatus } from '@/types/application';
import { Calendar, AlertCircle, Star, ChevronDown, Clock } from 'lucide-react';
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

const statusConfig: Record<TaskStatus, { label: string; buttonClass: string }> = {
  'todo': {
    label: 'To Do',
    buttonClass: 'bg-muted text-muted-foreground hover:bg-accent',
  },
  'in-progress': {
    label: 'In Progress',
    buttonClass: 'bg-[#f4d738] text-black hover:bg-[#f4d738]/90',
  },
  'complete': {
    label: 'Done',
    buttonClass: 'bg-[#90ee90] text-black hover:bg-[#90ee90]/90',
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
    <div className="border-2 border-border p-4 shadow-sm hover:shadow-md transition-shadow bg-card">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className={cn(
            "flex items-center justify-center w-8 h-8 font-mono font-bold text-sm border-2 border-border flex-shrink-0",
            isBonus ? "bg-[hsl(var(--status-bonus))] text-[hsl(var(--status-bonus-foreground))]" : "bg-primary text-primary-foreground"
          )}>
            {isBonus ? <Star className="h-4 w-4" /> : index + 1}
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-bold text-sm">{step.title}</h4>
            <p className="text-xs text-muted-foreground mb-2">{step.description}</p>
            {step.dueDate && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
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
                    ? "bg-muted text-muted-foreground cursor-not-allowed opacity-50" 
                    : statusConfig[currentStatus].buttonClass
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
          {step.priority === 'high' && currentStatus !== 'complete' && !isBonus && !isOverdue && (
            <AlertCircle className="h-4 w-4 text-red-600" />
          )}
        </div>
      </div>
      {isOverdue && (
        <div className="flex items-center gap-2 mt-3 pt-3 border-t-2 border-border">
          <Clock className="h-4 w-4 text-red-600" />
          <span className="text-sm font-mono font-bold text-red-600">Deadline passed</span>
        </div>
      )}
    </div>
  );
}
