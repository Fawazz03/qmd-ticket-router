"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PriorityBadge } from "@/components/priority-badge";
import { StatusBadge } from "@/components/status-badge";

interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  priority: "P1" | "P2" | "P3" | "P4";
  queue: string;
  status: "backlog" | "active" | "assigned";
  assigned_employee_name?: string | null;
  assigned_at?: string | null;
}

interface LiveTicketFlowProps {
  tickets: Ticket[];
}

export function LiveTicketFlow({
  tickets,
}: LiveTicketFlowProps) {
  const recentTickets = [...tickets]
    .reverse()
    .slice(0, 8);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Live Ticket Flow</CardTitle>
      </CardHeader>

      <CardContent>
        {recentTickets.length === 0 ? (
          <div className="py-8 text-center text-sm text-muted-foreground">
            No tickets in the system yet.
          </div>
        ) : (
          <div className="divide-y">
            {recentTickets.map((ticket) => (
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
                  <p className="truncate text-sm font-medium">
                    {ticket.title}
                  </p>

                  <p className="text-xs text-muted-foreground">
                    {ticket.queue}
                  </p>
                </div>

                <StatusBadge status={ticket.status} />

                <div className="w-32 shrink-0 text-right text-sm">
                  {ticket.assigned_employee_name ? (
                    <span className="font-medium">
                      {ticket.assigned_employee_name}
                    </span>
                  ) : (
                    <span className="text-muted-foreground">
                      Unassigned
                    </span>
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