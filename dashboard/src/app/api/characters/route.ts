// app/api/characters/route.ts
import { NextResponse } from 'next/server';
import clientPromise from '../../../lib/mongodb';

// Define the GET handler as a named export
export async function GET() {
  try {
    const client = await clientPromise;
    const db = client.db('rpgs');
    const characters = await db.collection('character').find({}).toArray();
    return NextResponse.json(characters);
  } catch (error) {
    console.error('Failed to fetch characters:', error);
    return NextResponse.json({ error: 'Failed to load data' }, { status: 500 });
  }
}
