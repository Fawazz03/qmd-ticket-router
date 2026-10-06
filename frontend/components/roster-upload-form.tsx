"use client";

import { useState } from "react";

import { uploadRoster } from "@/lib/api";

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

export function RosterUploadForm() {
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
      const data = await uploadRoster(file);

      setMessage(
        `Successfully uploaded ${data.total_employees} employees.`
      );

      setFile(null);
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Roster upload failed."
      );
    } finally {
      setUploading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Roster</CardTitle>

        <CardDescription>
          Upload the current shift roster in Excel format.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="roster-file">
            Roster Excel File
          </Label>

          <Input
            id="roster-file"
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
            : "Upload Roster"}
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