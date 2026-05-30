import mongoose from 'mongoose';

// Singleton pattern to avoid multiple connections during hot-reload in development
let cached: mongoose.Connection | null = null;

export async function connectToDatabase(): Promise<mongoose.Connection> {
  const uri = process.env.MONGODB_URI;

  if (!uri) {
    throw new Error('MONGODB_URI environment variable is not defined');
  }

  if (cached) {
    return cached;
  }

  await mongoose.connect(uri);
  cached = mongoose.connection;
  return cached;
}
