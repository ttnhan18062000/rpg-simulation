// app/api/combats/route.ts
import { NextResponse } from 'next/server';
import clientPromise from '../../../lib/mongodb';

// Define the GET handler for combat data
export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db('rpgs');
    const combats = await db.collection('combat').find({}).toArray();

    // Transform data for each combat
    const transformedCombats = combats.map(combat => {
      if (combat.data) {
        combat.data = Object.fromEntries(
          Object.entries(combat.data).map(([key, value]) => [key, value.length])
        );
      }
      return combat;
    });

    return NextResponse.json(transformedCombats);
  } catch (error) {
    console.error('Failed to fetch combats:', error);
    return NextResponse.json({ error: 'Failed to load data' }, { status: 500 });
  }
}