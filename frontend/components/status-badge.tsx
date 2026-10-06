import { Badge } from "@/components/ui/badge";

type TicketStatus =
  | "backlog"
  | "active"
  | "assigned";

interface StatusBadgeProps {
  status: TicketStatus;
}

export function StatusBadge({
  status,
}: StatusBadgeProps) {
  const styles: Record<TicketStatus, string> = {
    backlog:
      "border-slate-300 bg-slate-50 text-slate-700",

    active:
      "border-blue-300 bg-blue-50 text-blue-700",

    assigned:
      "border-green-300 bg-green-50 text-green-700",
  };

  const labels: Record<TicketStatus, string> = {
    backlog: "BACKLOG",
    active: "ACTIVE",
    assigned: "ASSIGNED",
  };

  return (
    <Badge
      variant="outline"
      className={styles[status]}
    >
      {labels[status]}
    </Badge>
  );
}