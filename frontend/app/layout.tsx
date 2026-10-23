import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'Object Stories — A Museum of Connections', description: 'Explore the stories and connections behind objects that shaped our world.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
