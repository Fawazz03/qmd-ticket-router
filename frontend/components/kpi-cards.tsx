import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface KpiCardsProps {
  backlog: number;
  active: number;
  assigned: number;
  simulationRunning: boolean;
}

export function KpiCards({
  backlog,
  active,
  assigned,
  simulationRunning,
}: KpiCardsProps) {
  const metrics = [
    {
      title: "Backlog",
      value: backlog,
      description: "Tickets waiting to arrive",
    },
    {
      title: "Active",
      value: active,
      description: "Tickets currently in flow",
    },
    {
      title: "Assigned",
      value: assigned,
      description: "Tickets successfully routed",
    },
    {
      title: "Simulation",
      value: simulationRunning ? "Running" : "Stopped",
      description: simulationRunning
        ? "Automatic ticket arrival is active"
        : "Simulation is currently stopped",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.title}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {metric.title}
            </CardTitle>
          </CardHeader>

          <CardContent>
            <div className="text-2xl font-semibold tracking-tight">
              {metric.value}
            </div>

            <p className="mt-1 text-xs text-muted-foreground">
              {metric.description}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}