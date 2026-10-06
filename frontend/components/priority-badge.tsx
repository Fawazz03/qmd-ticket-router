import { Badge } from "@/components/ui/badge";

type Priority = "P1" | "P2" | "P3" | "P4";

interface PriorityBadgeProps {
  priority: Priority;
}

export function PriorityBadge({
  priority,
}: PriorityBadgeProps) {
  const styles: Record<Priority, string> = {
    P1: "border-red-300 bg-red-50 text-red-700",
    P2: "border-orange-300 bg-orange-50 text-orange-700",
    P3: "border-yellow-300 bg-yellow-50 text-yellow-700",
    P4: "border-slate-300 bg-slate-50 text-slate-700",
  };

  return (
    <Badge
      variant="outline"
      className={styles[priority]}
    >
      {priority}
    </Badge>
  );
}