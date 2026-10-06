import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface RosterSummaryProps {
  total: number;
  agents: number;
  leads: number;
  queues: number;
}

export function RosterSummary({
  total,
  agents,
  leads,
  queues,
}: RosterSummaryProps) {
  const metrics = [
    {
      title: "Total Employees",
      value: total,
    },
    {
      title: "Agents",
      value: agents,
    },
    {
      title: "Leads",
      value: leads,
    },
    {
      title: "Active Queues",
      value: queues,
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
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
          </CardContent>
        </Card>
      ))}
    </div>
  );
}