"use client";

import { useEffect, useMemo, useState } from "react";

import { getTickets } from "@/lib/api";

import { PriorityBadge } from "@/components/priority-badge";
import { StatusBadge } from "@/components/status-badge";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { Badge } from "@/components/ui/badge";

type TicketStatus =
  | "backlog"
  | "active"
  | "assigned";

type Priority =
  | "P1"
  | "P2"
  | "P3"
  | "P4";

interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  priority: Priority;
  type?: string | null;
  queue: string;
  status: TicketStatus;
  assigned_employee_id?: number | null;
  assigned_employee_name?: string | null;
  created_at: string;
  arrived_at?: string | null;
  assigned_at?: string | null;
}

type StatusFilter =
  | "all"
  | "backlog"
  | "active"
  | "assigned";

function formatTime(timestamp?: string | null) {
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

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [filter, setFilter] =
    useState<StatusFilter>("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadTickets() {
    try {
      setLoading(true);
      setError("");

      const data = await getTickets();

      setTickets(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to load tickets."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTickets();

    const interval = setInterval(
      loadTickets,
      2000
    );

    return () => clearInterval(interval);
  }, []);

  const filteredTickets = useMemo(() => {
    if (filter === "all") {
      return tickets;
    }

    return tickets.filter(
      (ticket) => ticket.status === filter
    );
  }, [tickets, filter]);

  const counts = {
    all: tickets.length,
    backlog: tickets.filter(
      (ticket) => ticket.status === "backlog"
    ).length,
    active: tickets.filter(
      (ticket) => ticket.status === "active"
    ).length,
    assigned: tickets.filter(
      (ticket) => ticket.status === "assigned"
    ).length,
  };

  const filters: {
    value: StatusFilter;
    label: string;
  }[] = [
    {
      value: "all",
      label: "All",
    },
    {
      value: "backlog",
      label: "Backlog",
    },
    {
      value: "active",
      label: "Active",
    },
    {
      value: "assigned",
      label: "Assigned",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Tickets
        </h1>

        <p className="text-sm text-muted-foreground">
          Monitor ticket status and automatic routing
          assignments.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Ticket Queue</CardTitle>

          <CardDescription>
            Tickets are refreshed automatically while the
            simulation is running.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {filters.map((item) => (
              <button
                key={item.value}
                type="button"
                onClick={() => setFilter(item.value)}
                className={`rounded-md border px-3 py-1.5 text-sm transition-colors ${
                  filter === item.value
                    ? "border-primary bg-primary text-primary-foreground"
                    : "bg-background text-muted-foreground hover:bg-muted"
                }`}
              >
                {item.label}
                <span className="ml-2 text-xs opacity-70">
                  {counts[item.value]}
                </span>
              </button>
            ))}
          </div>

          {loading ? (
            <div className="py-10 text-center text-sm text-muted-foreground">
              Loading tickets...
            </div>
          ) : error ? (
            <div className="py-10 text-center text-sm text-destructive">
              {error}
            </div>
          ) : filteredTickets.length === 0 ? (
            <div className="py-10 text-center text-sm text-muted-foreground">
              No tickets found for this filter.
            </div>
          ) : (
            <div className="overflow-x-auto rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticket</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Queue</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Assigned To</TableHead>
                    <TableHead>Assigned At</TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {filteredTickets.map((ticket) => (
                    <TableRow key={ticket.id}>
                      <TableCell className="font-mono text-sm font-medium">
                        {ticket.ticket_number}
                      </TableCell>

                      <TableCell>
                        <PriorityBadge
                          priority={ticket.priority}
                        />
                      </TableCell>

                      <TableCell>
                        {ticket.queue}
                      </TableCell>

                      <TableCell>
                        <Badge variant="outline">
                          {ticket.type || "—"}
                        </Badge>
                      </TableCell>

                      <TableCell>
                        <StatusBadge
                          status={ticket.status}
                        />
                      </TableCell>

                      <TableCell className="font-medium">
                        {ticket.assigned_employee_name ||
                          "Unassigned"}
                      </TableCell>

                      <TableCell className="font-mono text-xs text-muted-foreground">
                        {formatTime(
                          ticket.assigned_at
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}