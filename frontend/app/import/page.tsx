"use client";

import { useState } from "react";

import { RosterUploadForm } from "@/components/roster-upload-form";
import { TicketUploadForm } from "@/components/ticket-upload-form";
import { SimulationControls } from "@/components/simulation-controls";

import {
  getSimulationState,
} from "@/lib/api";

interface SimulationState {
  batch_size: number;
  interval_seconds: number;
  running: boolean;
}

export default function ImportPage() {
  const [simulation, setSimulation] =
    useState<SimulationState>({
      batch_size: 1,
      interval_seconds: 5,
      running: false,
    });

  async function refreshSimulation() {
    try {
      const data = await getSimulationState();

      setSimulation(data);
    } catch (error) {
      console.error(
        "Failed to refresh simulation state:",
        error
      );
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Import & Simulation
        </h1>

        <p className="text-sm text-muted-foreground">
          Load the current roster, import the ticket backlog,
          and control ticket arrival simulation.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RosterUploadForm />

        <TicketUploadForm />
      </div>

      <SimulationControls
        running={simulation.running}
        batchSize={simulation.batch_size}
        intervalSeconds={simulation.interval_seconds}
        onSimulationChange={refreshSimulation}
      />
    </div>
  );
}