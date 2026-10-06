import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface TicketSummaryProps {
  total: number;
  backlog: number;
  active: number;
  assigned: number;
}

export function TicketSummary({
  total,
  backlog,
  active,
  assigned,
}: TicketSummaryProps) {
  const metrics = [
    {
      title: "Total Tickets",
      value: total,
    },
    {
      title: "Backlog",
      value: backlog,
    },
    {
      title: "Active",
      value: active,
    },
    {
      title: "Assigned",
      value: assigned,
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