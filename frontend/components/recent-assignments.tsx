"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { PriorityBadge } from "@/components/priority-badge";

interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  priority: "P1" | "P2" | "P3" | "P4";
  queue: string;
  status: string;
  assigned_employee_name?: string | null;
  assigned_at?: string | null;
}

interface RecentAssignmentsProps {
  tickets: Ticket[];
}

function formatAssignmentTime(
  timestamp?: string | null
) {
  if (!timestamp) {
    return "—";
  }

  return new Date(timestamp).toLocaleTimeString(
    [],
    {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }
  );
}

export function RecentAssignments({
  tickets,
}: RecentAssignmentsProps) {
  const assignments = tickets
    .filter(
      (ticket) =>
        ticket.status === "assigned" &&
        ticket.assigned_employee_name
    )
    .sort((a, b) => {
      const aTime = a.assigned_at
        ? new Date(a.assigned_at).getTime()
        : 0;

      const bTime = b.assigned_at
        ? new Date(b.assigned_at).getTime()
        : 0;

      return bTime - aTime;
    })
    .slice(0, 8);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Assignments</CardTitle>
      </CardHeader>

      <CardContent>
        {assignments.length === 0 ? (
          <div className="py-8 text-center text-sm text-muted-foreground">
            No assignments yet.
          </div>
        ) : (
          <div className="divide-y">
            {assignments.map((ticket) => (
              <div
                key={ticket.id}
                className="flex items-center gap-4 py-3"
              >
                <div className="w-20 shrink-0 font-mono text-sm font-medium">
                  {ticket.ticket_number}
                </div>

                <PriorityBadge
                  priority={ticket.priority}
                />

                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm">
                    {ticket.queue}
                  </p>
                </div>

                <div className="text-sm font-medium">
                  → {ticket.assigned_employee_name}
                </div>

                <div className="w-20 shrink-0 text-right font-mono text-xs text-muted-foreground">
                  {formatAssignmentTime(
                    ticket.assigned_at
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}