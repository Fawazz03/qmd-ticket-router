"use client";

import { useEffect, useState } from "react";

import { RosterSummary } from "@/components/roster-summary";

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

import { getRoster } from "@/lib/api";

interface Employee {
  id: number;
  name: string;
  role: string;
  shift_start: string;
  shift_end: string;
  queue: string;
}

export default function RosterPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadRoster() {
    try {
      setLoading(true);
      setError("");

      const data = await getRoster();

      setEmployees(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to load roster."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRoster();
  }, []);

  const agents = employees.filter(
    (employee) => employee.role === "agent"
  ).length;

  const leads = employees.filter(
    (employee) => employee.role === "lead"
  ).length;

  const queues = new Set(
    employees.map((employee) => employee.queue)
  ).size;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Current Roster
        </h1>

        <p className="text-sm text-muted-foreground">
          View the employees currently available to the
          ticket routing engine.
        </p>
      </div>

      <RosterSummary
        total={employees.length}
        agents={agents}
        leads={leads}
        queues={queues}
      />

      <Card>
        <CardHeader>
          <CardTitle>Employees</CardTitle>

          <CardDescription>
            Current shift assignments and routing queues.
          </CardDescription>
        </CardHeader>

        <CardContent>
          {loading ? (
            <div className="py-8 text-center text-sm text-muted-foreground">
              Loading roster...
            </div>
          ) : error ? (
            <div className="py-8 text-center text-sm text-destructive">
              {error}
            </div>
          ) : employees.length === 0 ? (
            <div className="py-8 text-center text-sm text-muted-foreground">
              No employees found.
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Employee</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Shift</TableHead>
                    <TableHead>Queue</TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {employees.map((employee) => (
                    <TableRow key={employee.id}>
                      <TableCell className="font-medium">
                        {employee.name}
                      </TableCell>

                      <TableCell>
                        <Badge variant="outline">
                          {employee.role === "lead"
                            ? "Lead"
                            : "Agent"}
                        </Badge>
                      </TableCell>

                      <TableCell className="font-mono text-sm">
                        {employee.shift_start} –{" "}
                        {employee.shift_end}
                      </TableCell>

                      <TableCell>
                        {employee.queue}
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