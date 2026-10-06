"use client";

import { useState } from "react";

import {
  configureSimulation,
  startSimulation,
  stopSimulation,
} from "@/lib/api";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface SimulationControlsProps {
  running: boolean;
  batchSize: number;
  intervalSeconds: number;
  onSimulationChange: () => void;
}

export function SimulationControls({
  running,
  batchSize,
  intervalSeconds,
  onSimulationChange,
}: SimulationControlsProps) {
  const [selectedBatchSize, setSelectedBatchSize] =
    useState(String(batchSize));

  const [selectedInterval, setSelectedInterval] =
    useState(String(intervalSeconds));

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleStart() {
    setLoading(true);
    setMessage("");

    try {
      await configureSimulation(
        Number(selectedBatchSize),
        Number(selectedInterval)
      );

      await startSimulation();

      setMessage("Simulation started.");
      onSimulationChange();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to start simulation."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleStop() {
    setLoading(true);
    setMessage("");

    try {
      await stopSimulation();

      setMessage("Simulation stopped.");
      onSimulationChange();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to stop simulation."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Simulation Controls</CardTitle>

        <CardDescription>
          Configure how tickets arrive from the backlog
          and start or stop automatic routing.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-5">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="batch-size">
              Batch Size
            </Label>

            <Select
              value={selectedBatchSize}
              onValueChange={(value) => {
                if (value !== null) {
                  setSelectedBatchSize(value);
                }
              }}
              disabled={running || loading}
            >
              <SelectTrigger id="batch-size">
                <SelectValue placeholder="Select batch size" />
              </SelectTrigger>

              <SelectContent>
                <SelectItem value="1">
                  1 ticket
                </SelectItem>

                <SelectItem value="2">
                  2 tickets
                </SelectItem>

                <SelectItem value="3">
                  3 tickets
                </SelectItem>

                <SelectItem value="5">
                  5 tickets
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="arrival-interval">
              Arrival Interval
            </Label>

            <Select
              value={selectedInterval}
              onValueChange={(value) => {
                if (value !== null) {
                  setSelectedInterval(value);
                }
              }}
              disabled={running || loading}
            >
              <SelectTrigger id="arrival-interval">
                <SelectValue placeholder="Select interval" />
              </SelectTrigger>

              <SelectContent>
                <SelectItem value="2">
                  Every 2 seconds
                </SelectItem>

                <SelectItem value="5">
                  Every 5 seconds
                </SelectItem>

                <SelectItem value="10">
                  Every 10 seconds
                </SelectItem>

                <SelectItem value="30">
                  Every 30 seconds
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex gap-3">
          <Button
            onClick={handleStart}
            disabled={running || loading}
          >
            {loading
              ? "Starting..."
              : "Start Simulation"}
          </Button>

          <Button
            variant="outline"
            onClick={handleStop}
            disabled={!running || loading}
          >
            {loading
              ? "Stopping..."
              : "Stop Simulation"}
          </Button>
        </div>

        {message && (
          <p className="text-sm text-muted-foreground">
            {message}
          </p>
        )}
      </CardContent>
    </Card>
  );
}