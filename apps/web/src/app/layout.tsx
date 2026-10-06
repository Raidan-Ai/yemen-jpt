import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'YemenJPT — Intelligence Platform',
  description: 'Sovereign Yemeni intelligence and knowledge platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <nav className="sticky top-0 z-10 border-b border-gray-200 bg-white shadow-sm">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-14 items-center justify-between">
              <a href="/" className="flex items-center gap-2">
                <span className="text-xl font-bold text-indigo-700">YemenJPT</span>
                <span className="hidden text-xs text-gray-400 sm:block">Intelligence Platform</span>
              </a>
              <div className="flex items-center gap-1 text-sm">
                {[['/', 'Dashboard'], ['/cases', 'Cases'], ['/research', 'Research'], ['/missions', 'Missions']].map(([href, label]) => (
                  <a key={href} href={href} className="rounded-md px-3 py-1.5 text-gray-600 hover:bg-gray-100 hover:text-indigo-700 transition-colors">{label}</a>
                ))}
              </div>
            </div>
          </div>
        </nav>
        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
      </body>
    </html>
  );
}