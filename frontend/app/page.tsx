"use client";

import { useEffect, useState } from "react";

import { KpiCards } from "@/components/kpi-cards";
import { LiveTicketFlow } from "@/components/live-ticket-flow";
import { RecentAssignments } from "@/components/recent-assignments";
import { SimulationStatusPill } from "@/components/simulation-status-pill";

import {
  getSimulationState,
  getTickets,
} from "@/lib/api";

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

interface SimulationState {
  batch_size: number;
  interval_seconds: number;
  running: boolean;
}

export default function DashboardPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [simulation, setSimulation] =
    useState<SimulationState>({
      batch_size: 1,
      interval_seconds: 5,
      running: false,
    });

  async function loadDashboard() {
    try {
      const [ticketData, simulationData] =
        await Promise.all([
          getTickets(),
          getSimulationState(),
        ]);

      setTickets(ticketData);
      setSimulation(simulationData);
    } catch (error) {
      console.error(
        "Failed to load dashboard:",
        error
      );
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(
      loadDashboard,
      2000
    );

    return () => clearInterval(interval);
  }, []);

  const backlog = tickets.filter(
    (ticket) => ticket.status === "backlog"
  ).length;

  const active = tickets.filter(
    (ticket) => ticket.status === "active"
  ).length;

  const assigned = tickets.filter(
    (ticket) => ticket.status === "assigned"
  ).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Operations Dashboard
          </h1>

          <p className="text-sm text-muted-foreground">
            Monitor ticket flow and automatic routing.
          </p>
        </div>

        <SimulationStatusPill
          running={simulation.running}
        />
      </div>

      <KpiCards
        backlog={backlog}
        active={active}
        assigned={assigned}
        simulationRunning={simulation.running}
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <LiveTicketFlow tickets={tickets} />

        <RecentAssignments tickets={tickets} />
      </div>
    </div>
  );
}