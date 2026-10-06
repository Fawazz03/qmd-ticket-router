import { Badge } from "@/components/ui/badge";

interface SimulationStatusPillProps {
  running: boolean;
}

export function SimulationStatusPill({
  running,
}: SimulationStatusPillProps) {
  return (
    <Badge
      variant="outline"
      className={
        running
          ? "gap-2 border-green-300 bg-green-50 text-green-700"
          : "gap-2 border-slate-300 bg-slate-50 text-slate-600"
      }
    >
      <span
        className={
          running
            ? "size-2 rounded-full bg-green-500 animate-pulse"
            : "size-2 rounded-full bg-slate-400"
        }
      />

      {running ? "Simulation Running" : "Simulation Stopped"}
    </Badge>
  );
}