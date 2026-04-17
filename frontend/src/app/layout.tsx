import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VERDIX — Autonomous Financial Decision Engine',
  description:
    'VERDIX passes a verdict on every transaction before executing it. Multi-agent AI with risk scoring, negotiation, memory, and autonomous USDC payments via Locus.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
