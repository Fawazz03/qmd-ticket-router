const API_BASE_URL = "http://localhost:8000";

export async function uploadRoster(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/roster/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Roster upload failed."
    );
  }

  return data;
}

export async function uploadTickets(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/tickets/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Ticket upload failed."
    );
  }

  return data;
}

export async function getTickets(status?: string) {
  const url = status
    ? `${API_BASE_URL}/api/tickets?status=${encodeURIComponent(status)}`
    : `${API_BASE_URL}/api/tickets`;

  const response = await fetch(url, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch tickets.");
  }

  return response.json();
}

export async function getRoster() {
  const response = await fetch(
    `${API_BASE_URL}/api/roster`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch roster.");
  }

  return response.json();
}

export async function getSimulationState() {
  const response = await fetch(
    `${API_BASE_URL}/api/simulation`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch simulation state."
    );
  }

  return response.json();
}

export async function configureSimulation(
  batchSize: number,
  intervalSeconds: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/simulation/configure`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        batch_size: batchSize,
        interval_seconds: intervalSeconds,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Failed to configure simulation."
    );
  }

  return data;
}

export async function startSimulation() {
  const response = await fetch(
    `${API_BASE_URL}/api/simulation/start`,
    {
      method: "POST",
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to start simulation."
    );
  }

  return data;
}

export async function stopSimulation() {
  const response = await fetch(
    `${API_BASE_URL}/api/simulation/stop`,
    {
      method: "POST",
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to stop simulation."
    );
  }

  return data;
}