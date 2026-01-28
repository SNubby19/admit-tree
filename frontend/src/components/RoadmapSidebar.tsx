import { ApplicationRoadmap, RoadmapCategory } from '@/types/application';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Map, Plus, Code, Briefcase, HeartPulse, Wrench, Palette, TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RoadmapSidebarProps {
  roadmaps: ApplicationRoadmap[];
  activeRoadmapId: string | null;
  onSelectRoadmap: (id: string) => void;
  onCreateRoadmap: () => void;
}

const categoryIcons: Record<RoadmapCategory, React.ComponentType<{ className?: string }>> = {
  'computer-science': Code,
  'business': Briefcase,
  'health-sciences': HeartPulse,
  'engineering': Wrench,
  'arts': Palette,
  'risk-analysis': TrendingUp,
};

const categoryColors: Record<RoadmapCategory, string> = {
  'computer-science': 'border-black',
  'business': 'border-black',
  'health-sciences': 'border-black',
  'engineering': 'border-black',
  'arts': 'border-black',
  'risk-analysis': 'border-black',
};

const categoryBackgrounds: Record<RoadmapCategory, string> = {
  'computer-science': '#87ceeb', // Sky blue
  'engineering': '#ff69b4',      // Hot pink
  'business': '#ffa07a',         // Light salmon
  'health-sciences': '#a388ee',  // Light purple
  'arts': '#b5d2ad',             // Light green
  'risk-analysis': '#ffa07a',    // Light salmon (reusing)
};

export function RoadmapSidebar({ 
  roadmaps, 
  activeRoadmapId, 
  onSelectRoadmap, 
  onCreateRoadmap 
}: RoadmapSidebarProps) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button 
          variant="outline" 
          size="sm" 
          className="gap-2 border-2 border-border font-bold uppercase tracking-wider text-xs"
        >
          <Map className="h-4 w-4" />
          Roadmaps
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-80 border-r-2 border-border">
        <SheetHeader className="border-b-2 border-border pb-4">
          <SheetTitle className="flex items-center gap-2 font-bold uppercase tracking-wider">
            <Map className="h-5 w-5" />
            Application Roadmaps
          </SheetTitle>
        </SheetHeader>
        
        <div className="mt-6 space-y-3">
          {roadmaps.map((roadmap) => {
            const Icon = categoryIcons[roadmap.category];
            const isActive = roadmap.id === activeRoadmapId;
            
            return (
              <button
                key={roadmap.id}
                onClick={() => onSelectRoadmap(roadmap.id)}
                className={cn(
                  'w-full p-4 text-left border-2 transition-all bg-card shadow-xs',
                  isActive 
                    ? 'border-primary shadow-md' 
                    : 'border-border hover:shadow-md'
                )}
                style={isActive ? { backgroundColor: '#fdfd96' } : undefined}
              >
                <div className="flex items-start gap-3">
                  <div 
                    className={cn('p-2 border-2', categoryColors[roadmap.category])}
                    style={{ backgroundColor: categoryBackgrounds[roadmap.category], color: '#000000' }}
                  >
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-sm truncate">{roadmap.name}</h4>
                    <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                      {roadmap.description}
                    </p>
                    <span className="text-xs font-mono text-muted-foreground mt-2 block">
                      {roadmap.programIds.length} programs
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        <div className="absolute bottom-6 left-6 right-6">
          <Button 
            onClick={onCreateRoadmap}
            className="w-full gap-2 border-2 border-border font-bold uppercase tracking-wider"
          >
            <Plus className="h-4 w-4" />
            New Roadmap
          </Button>
        </div>
      </SheetContent>
    </Sheet>
  );
}
