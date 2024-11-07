"use client"

import * as React from 'react';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid2';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

// Define TypeScript interface for combat data
interface Combat {
  _id: string ;
  id: string ;
  data: {
    Demon: number;
    Human: number;
  };
  event_type: string;
  type: string;
}

// CombatPage component
const CombatPage: React.FC = () => {
  const [combats, setCombats] = React.useState<Combat[]>([]);

  // Fetch function to load combat data
  const fetchCombats = async () => {
    try {
      const response = await fetch('/api/combats');
      const data: Combat[] = await response.json();
      setCombats(data);
    } catch (error) {
      console.error('Failed to fetch combats:', error);
    }
  };

  // Setup WebSocket connection on mount
  React.useEffect(() => {
    fetchCombats();

    const socket = new WebSocket('ws://localhost:3001'); // Adjust URL as needed

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    socket.onmessage = (event) => {
      console.log("Received update notification through WebSocket", event.data);
      const message = JSON.parse(event.data);
      if (message.type === 'event') {
        fetchCombats(); // Reload data on update notification
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <Paper sx={{ padding: 3 }}>
      <Grid container spacing={3}>
        {combats.map((combat) => {
          return (
            <Grid xs={12} sm={6} md={4} lg={3} key={combat._id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">Combat ID: {combat.id}</Typography>
                  <Typography variant="body2">Demon Count: {combat.data.Demon}</Typography>
                  <Typography variant="body2">Human Count: {combat.data.Human}</Typography>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Paper>
  );
};

export default CombatPage;