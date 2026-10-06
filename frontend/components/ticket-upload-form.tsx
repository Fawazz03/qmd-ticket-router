"use client";

import { useState } from "react";

import { uploadTickets } from "@/lib/api";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function TicketUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleUpload() {
    if (!file) {
      setMessage("Please select an Excel file.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      const data = await uploadTickets(file);

      setMessage(
        `Successfully uploaded ${data.total_tickets} tickets to the backlog.`
      );

      setFile(null);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Ticket upload failed."
      );
    } finally {
      setUploading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Ticket Backlog</CardTitle>

        <CardDescription>
          Upload tickets in Excel format. Tickets will remain
          in the backlog until the simulation releases them.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="ticket-file">
            Ticket Excel File
          </Label>

          <Input
            id="ticket-file"
            type="file"
            accept=".xlsx,.xls"
            onChange={(event) =>
              setFile(
                event.target.files?.[0] ?? null
              )
            }
          />
        </div>

        <Button
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading
            ? "Uploading..."
            : "Upload Tickets"}
        </Button>

        {message && (
          <p className="text-sm text-muted-foreground">
            {message}
          </p>
        )}
      </CardContent>
    </Card>
  );
}