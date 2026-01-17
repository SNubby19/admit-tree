import { Sparkles, Target, TrendingUp } from 'lucide-react';

interface DashboardHeaderProps {
  totalPrograms: number;
  overallProgress: number;
  completedTasks: number;
  totalTasks: number;
}

export function DashboardHeader({
  totalPrograms,
  overallProgress,
  completedTasks,
  totalTasks,
}: DashboardHeaderProps) {
  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-2">
        <div className="flex items-center justify-center w-10 h-10 bg-primary text-primary-foreground border-2 border-border">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">UniTrack Ontario</h1>
          <p className="text-muted-foreground text-sm">AI-Powered University Application Tracker</p>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
        <div className="bg-card border-2 border-border p-4 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-secondary border-2 border-border">
              <Target className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-bold font-mono">{totalPrograms}</p>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">Programs</p>
            </div>
          </div>
        </div>

        <div className="bg-card border-2 border-border p-4 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] border-2 border-border">
              <TrendingUp className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-bold font-mono">{overallProgress}%</p>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">Overall Progress</p>
            </div>
          </div>
        </div>

        <div className="bg-card border-2 border-border p-4 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] border-2 border-border">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <p className="text-2xl font-bold font-mono">{completedTasks}/{totalTasks}</p>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">Tasks Complete</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
