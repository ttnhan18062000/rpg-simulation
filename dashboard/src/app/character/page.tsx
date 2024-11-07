"use client"

import * as React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';

// Define TypeScript interfaces for character data
interface Character {
  _id: string;
  character_action: string;
  faction: string;
  info: string;
  is_alive: boolean;
  level: {
    current_level: number;
    current_exp: number;
    next_level_exp: number;
  };
  stats: {
    current_health: number;
    max_health: number;
    power: number;
    speed: number;
  };
  tile_id: number;
  type: string;
}

interface CharacterRow {
  id: string;
  character_action: string;
  faction: string;
  info: string;
  is_alive: boolean;
  current_level: number;
  current_exp: number;
  next_level_exp: number;
  current_health: number;
  max_health: number;
  power: number;
  speed: number;
  tile_id: number;
  type: string;
}

const columns: GridColDef[] = [
  { field: 'character_action', headerName: 'Action', width: 150 },
  { field: 'faction', headerName: 'Faction', width: 100 },
  { field: 'info', headerName: 'Info', width: 150 },
  { field: 'is_alive', headerName: 'Alive', width: 80, type: 'boolean' },
  { field: 'current_level', headerName: 'Level', width: 80, type: 'number' },
  { field: 'current_exp', headerName: 'Current EXP', width: 120, type: 'number' },
  { field: 'next_level_exp', headerName: 'Next Level EXP', width: 130, type: 'number' },
  { field: 'current_health', headerName: 'Current Health', width: 130, type: 'number' },
  { field: 'max_health', headerName: 'Max Health', width: 120, type: 'number' },
  { field: 'power', headerName: 'Power', width: 90, type: 'number' },
  { field: 'speed', headerName: 'Speed', width: 90, type: 'number' },
  { field: 'tile_id', headerName: 'Tile ID', width: 90, type: 'number' },
  { field: 'type', headerName: 'Type', width: 100 },
];

const CharacterDataGrid: React.FC = () => {
  const [rows, setRows] = React.useState<CharacterRow[]>([]);

  // Fetch function to reload character data
  const fetchCharacters = async () => {
    try {
      const response = await fetch('/api/characters');
      const data: Character[] = await response.json();

      const formattedData: CharacterRow[] = data.map((character) => ({
        id: character._id,
        character_action: character.character_action,
        faction: character.faction,
        info: character.info,
        is_alive: character.is_alive,
        current_level: character.level.current_level,
        current_exp: character.level.current_exp,
        next_level_exp: character.level.next_level_exp,
        current_health: character.stats.current_health,
        max_health: character.stats.max_health,
        power: character.stats.power,
        speed: character.stats.speed,
        tile_id: character.tile_id,
        type: character.type,
      }));

      setRows(formattedData);
    } catch (error) {
      console.error('Failed to fetch characters:', error);
    }
  };

  // Setup WebSocket connection on mount
  React.useEffect(() => {
    fetchCharacters();

    const socket = new WebSocket('ws://localhost:3001'); // Change this URL if needed

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onopen = function() {
        console.log("Connected to WebSocket server");
    };

    socket.onmessage = (event) => {
      console.log("Receive update notification through Websocket")
      const message = JSON.parse(event.data);
      if (message.type === 'update') {
        fetchCharacters(); // Reload data on update notification
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <Paper sx={{ height: 500, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{ border: 0 }}
      />
    </Paper>
  );
};

export default CharacterDataGrid;