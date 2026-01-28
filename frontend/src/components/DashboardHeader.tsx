import { Sparkles, Target, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';

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
  const [userName, setUserName] = useState<string>('');

  useEffect(() => {
    // Try to get user name from localStorage
    try {
      const storedRoadmap = localStorage.getItem("currentRoadmap");
      if (storedRoadmap) {
        const roadmap = JSON.parse(storedRoadmap);
        if (roadmap.student_profile?.name) {
          setUserName(roadmap.student_profile.name);
        }
      }
    } catch (error) {
      console.error("Failed to load user name:", error);
    }
  }, []);

  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-2">
        <div className="flex items-center justify-center w-10 h-10 bg-black text-white border-2 border-border">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
            Welcome back{userName ? `, ${userName}` : ''}!
          </h1>
          <p className="text-muted-foreground text-sm">Track your current programs</p>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
        <div className="bg-card border-2 border-border p-4 shadow-xs">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 border-2 border-border" style={{ backgroundColor: '#ff69b4', color: '#000000' }}>
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
            <div className="flex items-center justify-center w-10 h-10 border-2 border-border" style={{ backgroundColor: '#ffa07a', color: '#000000' }}>
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
            <div className="flex items-center justify-center w-10 h-10 border-2 border-border" style={{ backgroundColor: '#a7dbd8', color: '#000000' }}>
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
