import { BonusTask, TaskStatus } from '@/types/application';
import { Check, Star, BookOpen, Award, Heart, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface BonusTaskCardProps {
  task: BonusTask;
  onStatusChange?: (newStatus: TaskStatus) => void;
}

const categoryConfig = {
  extracurricular: { icon: Star, label: 'Extracurricular' },
  academic: { icon: BookOpen, label: 'Academic' },
  leadership: { icon: Award, label: 'Leadership' },
  community: { icon: Heart, label: 'Community' },
};

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

export function BonusTaskCard({ task, onStatusChange }: BonusTaskCardProps) {
  const { icon: Icon, label } = categoryConfig[task.category];
  const currentStatus: TaskStatus = task.status || 'todo';

  const handleStatusChange = (newStatus: TaskStatus) => {
    if (onStatusChange) {
      onStatusChange(newStatus);
    }
  };

  return (
    <div className="bg-card border-2 border-border p-4 shadow-sm hover:shadow-md transition-all">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          {/* <div className="flex items-center justify-center w-8 h-8 bg-[hsl(var(--status-bonus))] text-[hsl(var(--status-bonus-foreground))] border-2 border-border flex-shrink-0">
            <Star className="h-4 w-4" />
          </div> */}
          <div className="flex-1 min-w-0">
            <h4 className="font-bold text-sm">{task.title}</h4>
            <p className="text-xs text-muted-foreground mb-2">{task.description}</p>
            <div className="flex items-center gap-1.5">
              <Icon className="h-3 w-3 text-[hsl(var(--status-bonus))]" />
              <span className="text-xs font-mono font-bold text-[hsl(var(--status-bonus))] uppercase">
                {label}
              </span>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button 
                className={cn(
                  "inline-flex items-center gap-1 px-2 py-0.5 text-xs font-mono font-bold uppercase tracking-wider border-2 border-border transition-colors",
                  statusConfig[currentStatus].buttonClass
                )}
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
        </div>
      </div>
    </div>
  );
}
